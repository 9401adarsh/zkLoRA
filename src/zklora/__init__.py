__version__ = "0.1.2"

__all__ = [
    "batch_verify_proofs",
    "LoRAServer",
    "LoRAServerSocket",
    "BaseModelClient",
    "commit_activations",
    "verify_commitment",
    "__version__",
]


def _ensure_transformers_peft_compat() -> None:
    import transformers

    if hasattr(transformers, "EncoderDecoderCache"):
        return

    cache_base = getattr(transformers, "Cache", object)

    class EncoderDecoderCache(cache_base):
        pass

    transformers.EncoderDecoderCache = EncoderDecoderCache


def __getattr__(name):
    if name == "batch_verify_proofs":
        from .zk_proof_generator import batch_verify_proofs

        return batch_verify_proofs
    if name in {"LoRAServer", "LoRAServerSocket"}:
        _ensure_transformers_peft_compat()
        from .lora_contributor_mpi import LoRAServer, LoRAServerSocket

        return {"LoRAServer": LoRAServer, "LoRAServerSocket": LoRAServerSocket}[name]
    if name == "BaseModelClient":
        from .base_model_user_mpi import BaseModelClient

        return BaseModelClient
    if name in {"commit_activations", "verify_commitment"}:
        from .polynomial_commit import commit_activations, verify_commitment

        return {
            "commit_activations": commit_activations,
            "verify_commitment": verify_commitment,
        }[name]
    raise AttributeError(f"module 'zklora' has no attribute {name!r}")
