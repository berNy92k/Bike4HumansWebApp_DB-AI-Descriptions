from pydantic import BaseModel, Field

from app.models.bike import BikeColor, BikeType, BikeUsage, BrakeType, FrameMaterial, FrameSizeLabel, \
    SuspensionType, TargetUser


class BikeAutoTagResponseDto(BaseModel):
    bike_type: BikeType | None = Field(default=None)
    frame_material: FrameMaterial | None = Field(default=None)
    frame_size_label: FrameSizeLabel | None = Field(default=None)
    brake_type: BrakeType | None = Field(default=None)
    suspension_type: SuspensionType | None = Field(default=None)
    color: BikeColor | None = Field(default=None)
    usage: BikeUsage | None = Field(default=None)
    target_user: TargetUser | None = Field(default=None)
