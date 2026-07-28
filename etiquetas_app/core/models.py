from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExtractConfig:
    crop_left_ratio: float = 0.64
    crop_top_ratio: float = 0.0
    crop_right_ratio: float = 1.0
    crop_bottom_ratio: float = 0.13
    render_scale: int = 3

    def to_dict(self) -> dict:
        return {
            "crop_left_ratio": self.crop_left_ratio,
            "crop_top_ratio": self.crop_top_ratio,
            "crop_right_ratio": self.crop_right_ratio,
            "crop_bottom_ratio": self.crop_bottom_ratio,
            "render_scale": self.render_scale,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExtractConfig":
        return cls(
            crop_left_ratio=float(data.get("crop_left_ratio", 0.64)),
            crop_top_ratio=float(data.get("crop_top_ratio", 0.0)),
            crop_right_ratio=float(data.get("crop_right_ratio", 1.0)),
            crop_bottom_ratio=float(data.get("crop_bottom_ratio", 0.13)),
            render_scale=int(data.get("render_scale", 3)),
        )


@dataclass
class SplitConfig:
    pages_per_group: int = 2

    def to_dict(self) -> dict:
        return {"pages_per_group": self.pages_per_group}

    @classmethod
    def from_dict(cls, data: dict) -> "SplitConfig":
        return cls(pages_per_group=int(data.get("pages_per_group", 2)))


@dataclass
class OverlayConfig:
    image_scale: int = 2
    image_width: int = 100
    image_height: int = 50
    offset_x: int = 10
    offset_y: int = 10

    def to_dict(self) -> dict:
        return {
            "image_scale": self.image_scale,
            "image_width": self.image_width,
            "image_height": self.image_height,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OverlayConfig":
        return cls(
            image_scale=int(data.get("image_scale", 2)),
            image_width=int(data.get("image_width", 100)),
            image_height=int(data.get("image_height", 50)),
            offset_x=int(data.get("offset_x", 10)),
            offset_y=int(data.get("offset_y", 10)),
        )


@dataclass
class AppConfig:
    paths: dict = field(default_factory=lambda: {
        "default_output": "~/Downloads/ETIQUETAS",
        "images_folder": "~/Downloads/IMAGENES ETIQUETAS",
    })
    extract: ExtractConfig = field(default_factory=ExtractConfig)
    split: SplitConfig = field(default_factory=SplitConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    theme: str = "dark"

    def to_dict(self) -> dict:
        return {
            "paths": dict(self.paths),
            "extract": self.extract.to_dict(),
            "split": self.split.to_dict(),
            "overlay": self.overlay.to_dict(),
            "theme": self.theme,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        return cls(
            paths=dict(data.get("paths", {
                "default_output": "~/Downloads/ETIQUETAS",
                "images_folder": "~/Downloads/IMAGENES ETIQUETAS",
            })),
            extract=ExtractConfig.from_dict(data.get("extract", {})),
            split=SplitConfig.from_dict(data.get("split", {})),
            overlay=OverlayConfig.from_dict(data.get("overlay", {})),
            theme=str(data.get("theme", "dark")),
        )
