# --- XFORMERS SAFE MOCK OPS ---
import torch

def memory_efficient_attention(q, k, v, attn_bias=None, p=0.0, scale=None):
    try:
        return torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=attn_bias, dropout_p=p)
    except:
        return torch.matmul(q, k.transpose(-1, -2))

class fmha:
    class attn_bias:
        class BlockDiagonalMask:
            @staticmethod
            def from_seqlens(*args, **kwargs):
                return None
