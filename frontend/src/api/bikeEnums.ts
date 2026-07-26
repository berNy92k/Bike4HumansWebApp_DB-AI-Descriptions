// Mirrors the str-enum classes in app/models/bike.py (enums are not enforced at the DB layer
// there either, so this is a UI convenience for the select inputs, not a validation boundary).
export const BIKE_TYPES = ['MOUNTAIN', 'ROAD', 'GRAVEL', 'CITY', 'TREKKING', 'ELECTRIC', 'BMX', 'CHILDREN']
export const FRAME_MATERIALS = ['ALUMINIUM', 'CARBON', 'STEEL', 'TITANIUM']
export const FRAME_SIZE_LABELS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
export const BRAKE_TYPES = ['V_BRAKE', 'MECHANICAL_DISC', 'HYDRAULIC_DISC', 'RIM', 'COASTER']
export const SUSPENSION_TYPES = ['NONE', 'FRONT', 'FULL']
export const BIKE_USAGES = ['CITY', 'COMMUTING', 'SPORT', 'TOURING', 'TRAIL', 'OFF_ROAD']
export const TARGET_USERS = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'PROFESSIONAL']
export const BIKE_COLORS = ['BLACK', 'WHITE', 'RED', 'BLUE', 'GREEN', 'GREY', 'YELLOW', 'ORANGE', 'PINK', 'PURPLE']
