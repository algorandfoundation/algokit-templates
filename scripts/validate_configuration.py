import fire  # type: ignore[import-untyped]
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
import yaml
from pathlib import Path


class ExampleType(str, Enum):
    FRONTEND = "frontend"
    SMART_CONTRACT = "smart-contract"
    FULLSTACK = "fullstack"
    NOTEBOOK = "notebook"


class TemplateData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str = Field(description="Path to the source template file")
    data: Optional[Dict[str, Optional[str | bool]]] = Field(
        default=None,
        description="Optional dictionary of template variables and their values",
    )
    destination: Optional[str] = Field(
        default=None,
        description="Optional custom destination path for the processed template",
    )


class Example(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(
        description="Unique identifier for the example. This will be use for the example's directory name."
    )
    project_name: str = Field(description="Name of the project")
    type: ExampleType = Field(
        description="Category of the example (frontend, smart-contract, or dapp)"
    )
    author: str = Field(description="Name  or organization of the example's author")
    title: str = Field(description="Title of the example")
    description: str = Field(description="Detailed description of the example")
    image: Optional[str] = Field(
        default=None, description="URL to the example's preview image"
    )
    tags: List[str] = Field(description="List of relevant tags/keywords")
    features: List[str] = Field(description="List of key features demonstrated")
    templates: List[TemplateData] = Field(description="List of template configurations")
    detailsPages: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional dictionary of detail page paths (e.g., smartContract)",
    )

    @field_validator("detailsPages")
    @classmethod
    def validate_details_pages_paths(cls, v):
        if v is not None:
            for key, path in v.items():
                if not Path(path).exists():
                    raise ValueError(f"Path does not exist for {key}: {path}")
        return v


class Examples(BaseModel):
    model_config = ConfigDict(extra="forbid")
    examples: List[Example] = Field(description="List of all example projects")


def validate_examples(examples_yml_path: str = "examples/examples.yml"):
    examples_path = Path(examples_yml_path)
    print(f"Validating examples from {examples_path}")

    try:
        with open(examples_path, "r") as f:
            data = yaml.safe_load(f)

        # Validate the data against the Examples model
        Examples(**data)
        print("✅ Configuration is valid!")
        return True

    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False


if __name__ == "__main__":
    fire.Fire(validate_examples)
