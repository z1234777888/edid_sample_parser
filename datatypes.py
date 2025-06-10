from typing import TypedDict


class HeaderInfoData(TypedDict):
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


class DP_DescriptorInfo(TypedDict, total=False):
    SerialNumber: str
    AsciiString: str
    ProductName: str
    max_resolution: str
    max_refresh_rate: str


class DTDInfoData(TypedDict, total=False):
    perfered_timing: str
    dtd_timing: list[str]
    dp_descriptor: DP_DescriptorInfo


class TimingInfoData(TypedDict):
    Standard: list[StaTimingItem]
    Established_1: list[EstTimingItem]
    Established_2: list[EstTimingItem]


class StandardBlockResult(TypedDict):
    HeaderInfo: HeaderInfoData
    TimingInfo: TimingInfoData
    DTDInfo: DTDInfoData


class CTABlockResult(TypedDict):
    TagCodeInfo: list[dict[str, str]]
    DTDInfo: DTDInfoData


class DisplayIDBlockResult(TypedDict):
    Type_I: list[str]


class TotalResult(TypedDict, total=False):
    StandardBlockInfo: StandardBlockResult
    CTABlockInfo: CTABlockResult
    DisplayIDBlockInfo: DisplayIDBlockResult
