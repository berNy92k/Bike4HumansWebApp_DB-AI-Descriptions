import enum

from sqlalchemy import String, Text, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Bike(BaseModel):
    __tablename__ = "bikes"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_description_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    bike_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    frame_material: Mapped[str | None] = mapped_column(String(100), nullable=True)
    frame_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frame_size_label: Mapped[str | None] = mapped_column(String(20), nullable=True)

    wheel_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tire_width: Mapped[int | None] = mapped_column(Integer, nullable=True)

    gear_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    brake_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    suspension_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    color: Mapped[str | None] = mapped_column(String(255), nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    recommended_height_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recommended_height_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    usage: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_user: Mapped[str | None] = mapped_column(String(100), nullable=True)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"), nullable=False)


class BikeType(str, enum.Enum):
    MOUNTAIN = "MOUNTAIN"
    ROAD = "ROAD"
    GRAVEL = "GRAVEL"
    CITY = "CITY"
    TREKKING = "TREKKING"
    ELECTRIC = "ELECTRIC"
    BMX = "BMX"
    CHILDREN = "CHILDREN"


class FrameMaterial(str, enum.Enum):
    ALUMINIUM = "ALUMINIUM"
    CARBON = "CARBON"
    STEEL = "STEEL"
    TITANIUM = "TITANIUM"


class FrameSizeLabel(str, enum.Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class BrakeType(str, enum.Enum):
    V_BRAKE = "V_BRAKE"
    MECHANICAL_DISC = "MECHANICAL_DISC"
    HYDRAULIC_DISC = "HYDRAULIC_DISC"
    RIM = "RIM"
    COASTER = "COASTER"


class SuspensionType(str, enum.Enum):
    NONE = "NONE"
    FRONT = "FRONT"
    FULL = "FULL"


class BikeUsage(str, enum.Enum):
    CITY = "CITY"
    COMMUTING = "COMMUTING"
    SPORT = "SPORT"
    TOURING = "TOURING"
    TRAIL = "TRAIL"
    OFF_ROAD = "OFF_ROAD"


class TargetUser(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    PROFESSIONAL = "PROFESSIONAL"


class BikeColor(str, enum.Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    GREY = "GREY"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    PINK = "PINK"
    PURPLE = "PURPLE"
