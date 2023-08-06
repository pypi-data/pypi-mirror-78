import torch
from torch.optim.optimizer import Optimizer, required

required = object()

class FBA(Optimizer):
  def __init__(self, params, lr=required, regularization_param=1e-5):
    if lr is not required and lr < 0.0:
        raise ValueError("Invalid learning rate: {}".format(lr))

    defaults = dict(lr=lr, lam=regularization_param)
    super(FBA, self).__init__(params, defaults)

  def __setstate__(self, state):
    super(FBA, self).__setstate__(state)
  
  def forward_part(self, p, d_p, group):
    return p.add_(d_p, alpha=-group['lr'])
  
  def backward_part(self, p, group):
    u = p.abs().add(-group['lam'])
    return p.sign_().mul_(torch.max(u,torch.zeros_like(u)))

  @torch.no_grad()
  def step(self):
    loss = None
    for group in self.param_groups:
      for p in group['params']:
        if p.grad is None:
          print('grad is None!')
          continue
        d_p = p.grad
        if d_p.is_sparse:
            raise RuntimeError('FBA does not support sparse gradients')
            
        ### FORWARD PART
        self.forward_part(p, d_p, group)
        ### BACKWARD PART
        self.backward_part(p, group)

    return loss
    
class PISFBA(FBA):
  def __init__(self, params, lr=required, regularization_param=1e-5, beta=[0.9], gamma=[0.9], theta=[0.5]):
    if lr is not required and lr < 0.0:
      raise ValueError("Invalid learning rate: {}".format(lr))
    if isinstance(beta, list) == False:
      raise ValueError("Invalid control sequences beta, it should be list.")
    if isinstance(gamma, list) == False:
      raise ValueError("Invalid control sequences gamma, it should be list.")
    if isinstance(theta, list) == False:
      raise ValueError("Invalid control sequences theta, it should be list.")

    defaults = dict(lr=lr, lam=regularization_param, beta=beta, gamma=gamma, theta=theta)
    super(FBA, self).__init__(params, defaults)

  def __setstate__(self, state):
    super(PISFBA, self).__setstate__(state)
  
  def _FBO(self, Tx, d_p, group):
    ### FORWARD PART
    self.forward_part(Tx, d_p, group)
    ### BACKWARD PART
    self.backward_part(Tx, group)

  @torch.no_grad()
  def extrastep(self):
    group_idx = 0
    for group in self.param_groups:
      _gammas = group['gamma']
      _thetas = group['theta']

      group_idx += 1
      state = self.state['group ' + str(group_idx)]
      if len(state)==0:
        state['step'] = 0
        state['previous_p'] = []
        state['previous_dp'] = []
        state['Ty'] = []
      param_idx = -1
      state_p = state['previous_p']
      state_dp = state['previous_dp']
      state_Ty = state['Ty']

      conseq_idx = state['step']
      try:
        gamma = _gammas[conseq_idx]
      except:
        gamma = _gammas[-1]

      try:
        theta = _thetas[conseq_idx]
      except:
        theta = _thetas[-1]

      for p in group['params']:
        param_idx += 1
        if p.grad is None:
          print('p.grad is none')
          continue
        d_p = p.grad

        if d_p.is_sparse:
          raise RuntimeError('PISFBA does not support sparse gradients')

        if state['step']==0:
          p0 = p.clone()
          d_p0 = d_p.clone()
          state_p.append(p0)
          state_dp.append(d_p0)
        else:
          p0 = state_p[param_idx]
          d_p0 = state_dp[param_idx]
        
        ### update y_n
        y = p.clone()
        y.mul_(1+theta).add_(p0, alpha=-theta)

        ## update Ty_n
        d_y = d_p.clone()
        d_y.mul_(1+theta).add_(d_p0, alpha=-theta)
        Ty = y.clone()
        self._FBO(Ty, d_y, group)

        if state['step']==0:
          state_Ty.append(Ty)
        else:
          state_Ty[param_idx] = Ty

        ### update z_n
        z = p.clone()
        Tx = p.clone()
        self._FBO(Tx, d_p, group)
        z.mul_(1-gamma).add_(Tx, alpha=gamma)

        ### update parameter
        state_p[param_idx] = p
        state_dp[param_idx] = d_p
        p.mul_(torch.zeros_like(p)).add_(z)

      state['step'] += 1

  @torch.no_grad()
  def step(self):
    loss = None

    group_idx = 0
    for group in self.param_groups:
      _betas = group['beta']

      group_idx += 1
      state = self.state['group ' + str(group_idx)]
      if len(state)==0:
        raise RuntimeError('Need to call extrastep before calling step.')
      param_idx = -1
      state_Ty = state['Ty']

      conseq_idx = state['step'] - 1
      try:
        beta = _betas[conseq_idx]
      except:
        beta = _betas[-1]

      for p in group['params']:
        param_idx += 1
        if p.grad is None:
          print('p.grad is none')
          continue
        d_p = p.grad # p is z_n in step

        if d_p.is_sparse:
          raise RuntimeError('PISFBA does not support sparse gradients')

        ## Ty_n from extrastep
        Ty = state_Ty[param_idx]

        ### update Tz_n
        Tz = p.clone()
        self._FBO(Tz, d_p, group)

        ### update parameter
        p.mul_(torch.zeros_like(p)).add_(Ty).mul_(1-beta).add_(Tz, alpha=beta)

    return loss