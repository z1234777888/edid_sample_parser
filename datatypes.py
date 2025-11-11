from typing import TypedDict


class HeaderInfoData(TypedDict, total=False):
    MF_id: str
    product_code: str
    serial_number: str
    MF_week: str
    MF_year: str
    version: str


class StaTimingItem(TypedDict):
    h_res: str
    v_res: str
    refresh_rate: str
    aspect_ratio: str


class EstTimingItem(TypedDict):
    resolution: str
    refresh_rate: str
    source: str


class DTDInfoData(TypedDict, total=False):
    perferred_timing: str
    dtd_timing: list[str]
    dp_descriptor: dict[str, dict[str, str]]


class TimingInfoData(TypedDict):
    Standard: list[StaTimingItem]
    Established_1: list[EstTimingItem]
    Established_2: list[EstTimingItem]


class StandardBlockResult(TypedDict, total=False):
    HeaderInfo: HeaderInfoData
    TimingInfo: TimingInfoData
    DTDInfo: DTDInfoData


class CTABlockResult(TypedDict):
    TagCodeInfo: list[dict[str, str]]
    DTDInfo: DTDInfoData
    dtd_offset: int


class DisplayIDBlockResult(TypedDict):
    Type_I: list[str]


class TotalResult(TypedDict, total=False):
    StandardBlockInfo: StandardBlockResult
    CTABlockInfo: CTABlockResult
    DisplayIDBlockInfo: DisplayIDBlockResult
    EDIDRawData: str
    Checksum: list[str]
    ExtensionNum: str
    check_dtd_offset: str
