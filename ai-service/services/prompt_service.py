from pathlib import Path


class PromptService:
    def __init__(self, prompts_dir: str):
        self._prompts_dir = Path(prompts_dir)

    def load(self, prompt_name: str) -> str:
        prompt_path = self._prompts_dir / prompt_name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_name}")
        return prompt_path.read_text(encoding="utf-8")
