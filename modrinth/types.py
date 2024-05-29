from dataclasses import dataclass
from typing import Any, Optional, Self
from enum import Enum, Flag, auto
from datetime import datetime
from pathlib import Path

class req_method(Enum):
    GET = 0
    POST = 1
    DOWNLOAD = 2

GET = req_method.GET
POST = req_method.POST
DOWNLOAD = req_method.DOWNLOAD

@dataclass
class endpoint:
    method: req_method
    endpoint: Path

class Required(str, Enum):
    Required = "required"
    Optional = "optional"
    Unsupported = "unsupported"

class Status(str, Enum):
    Approved = "approved"
    Archived = "archived"
    Rejected = "rejected"
    Draft = "draft"
    Unlisted = "unlisted"
    Processing = "processing"
    Withheld = "withheld"
    Scheduled = "scheduled"
    Private = "private"
    Unknown = "unknown"

class RequestedStatus(str, Enum):
    Approved = "approved"
    Archived = "archived"
    Unlisted = "unlisted"
    Private = "private"
    Draft = "draft"

class ProjectType(str, Enum):
    Mod = "mod"
    Modpack = "modpack"
    Resourcepack = "resourcepack"
    Shader = "shader"

class MonetizationStatus(str, Enum):
    Monetized = "monetized"
    Demonetized = "demonetized"
    ForceDemonetized = "force-demonetized"

class VersionType(str, Enum):
    Release = "release"
    Beta = "beta"
    Alpha = "alpha"

@dataclass
class GalleryImage:
    """
    :param str url: The URL of the gallery image
    :param bool featured: Whether the image is featured in the gallery
    :param str|None title: The title of the gallery image
    :param str|None description: The description of the gallery image
    :param datetime.datetime: The date and time the gallery image was created
    :param int ordering: The order of the gallery image. Gallery images are sorted by this field and then alphabetically by title.
    """
    url: str
    featured: bool
    created: datetime
    title: Optional[str] = None
    description: Optional[str] = None
    ordering: Optional[int] = None

@dataclass
class ProjectLicense:
    """
    :param str id: The SPDX license ID of a project
    :param str name: The long name of a license
    :param str url: The URL to this license
    """
    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None

@dataclass
class ProjectDonationURL:
    """
    :param str id: The ID of the donation platform
    :param str platform: The donation platform this link is to
    :param str url: The URL of the donation platform and user
    """
    id: str
    platform: str
    url: str

@dataclass
class VersionFileHashes:
    sha512: str
    sha1: str

class VersionFileType(str, Enum):
    """
    The type of the additional file, used mainly for adding resource packs to datapacks
    """
    RequiredResourcePack = "required-resource-pack"
    OptionalReqourcePack = "optional-resource-pack"

@dataclass
class VersionFile:
    hashes: VersionFileHashes
    url: str
    filename: str
    primary: bool
    size: int
    file_type: Optional[VersionFileType] = None

class VersionDepencencyType(str, Enum):
    """
    The type of dependency that this version has
    """
    Required = "required"
    Optional = "optional"
    Incompatible = "incompatible"
    Embedded = "embedded"

@dataclass
class VersionDepencency:
    dependency_type: VersionDepencencyType
    version_id: Optional[str] = None
    project_id: Optional[str] = None
    file_name: Optional[str] = None 

class UserBadges(Flag):
    """
    User badges bitfield
    """
    _UNUSED = auto()
    EARLY_MODPACK_ADOPTER = auto()
    EARLY_RESPACK_ADOPTER = auto()
    EARLY_PLUGIN_ADOPTER = auto()
    ALPHA_TESTER = auto()
    CONTRIBUTOR = auto()
    TRANSLATOR = auto()

class UserRole(str, Enum):
    Admin = "admin"
    Moderator = "moderator"
    Developer = "developer"

class UserPayoutWallet(str, Enum):
    Paypal = "paypal"
    Venmo = "venmo"

class UserPayoutWalletType(str, Enum):
    Email = "email"
    Phone = "phone"
    UserHandle = "user_handle"

@dataclass
class UserPayoutData:
    balance: Optional[int] = None
    payout_wallet: Optional[UserPayoutWallet] = None
    payout_wallet_type: Optional[UserPayoutWalletType] = None
    payout_adress: Optional[str] = None

class TeamMemberPermissions(Flag):
    """
    Team member permissions bitfield
    """
    UPLOAD_VERSION = auto()
    DELETE_VERSION = auto()
    EDIT_DETAILS = auto()
    EDIT_BODY = auto()
    MANAGE_INVITES = auto()
    REMOVE_MEMBER = auto()
    EDIT_MEMBER = auto()
    DELETE_PROJECT = auto()
    VIEW_ANALYTICS = auto()
    VIEW_PAYOUTS = auto()

#-========================================================================================================================================================================-
# Models:

@dataclass
class Project:
    """
    :param str slug: The slug of a project, used for vanity URLs.
    :param str title: The title or name of the project.
    :param str description: A short description of the project.
    :param list[str] categories: A list of the categories that the project has.
    :param modrinth.types.Required client_side: The client side support of the project
    :param modrinth.types.Required server_side: The server side support of the project
    :param str body: A long form description of the project
    :param modrinth.types.Status status: The status of the project
    :param modrinth.types.RequestedStatus: The requested status when submitting for review or scheduling the project for release
    :param list[str] additional_categories: A list of categories which are searchable but non-primary
    :param str|None issues_url: An optional link to where to submit bugs or issues with the project
    :param str|None source_url: An optional link to the source code of the project
    :param str|None wiki_url: An optional link to the project's wiki page or other relevant information
    :param str|None discord_url: An optional invite link to the project's discord
    :param list[modrinth.types.ProjectDonationURL] donation_urls: A list of donation links for the project
    :param modrinth.types.ProjectType project_type: The project type of the project
    :param int downloads: The total number of downloads of the project
    :param str|None icon_url: The URL of the project's icon
    :param int|None color: The RGB color of the project, automatically generated from the project icon
    :param str thread_ir: The ID of the moderation thread associated with this project
    :param modrinth.types.MonetizationStatus monetization_status:
    :param str id: The ID of the project, encoded as a base62 string
    :param str team: The ID of the team that has ownership of this project
    :param object|None moderator_message: A message that a moderator sent regarding the project !!!DEPRECATED!!!
    :param datetime.datetime published: The date the project was published
    :param datetime.datetime updated: The date the project was last updated
    :param datetime.datetime|None approved: The date the project's status was set to an approved status
    :param datetime.datetime|None queued: The date the project's status was submitted to moderators for review
    :param int followers: The total number of users following the project
    :param modrinth.types.ProjectLicense license: The license of the project
    :param list[str] versions: A list of the version IDs of the project (will never be empty unless draft status)
    :param list[str] game_versions: A list of all of the game versions supported by the project
    :param list[str] loaders: A list of all of the loaders supported by the project
    :param list[modrinth.types.GalleryImage] gallery: A list of images that have been uploaded to the project's gallery 
    """
    slug: str
    title: str
    description: str
    client_side: Required
    server_side: Required
    body: str
    status: Status
    project_type: ProjectType
    downloads: int
    id: str
    team: str
    published: datetime
    updated: datetime
    followers: int
    categories: Optional[list[str]] = None
    requested_status: Optional[RequestedStatus] = None
    additional_categories: Optional[list[str]] = None
    issues_url: Optional[str] = None
    source_url: Optional[str] = None
    wiki_url: Optional[str] = None
    discord_url: Optional[str] = None
    donation_urls: Optional[ProjectDonationURL] = None
    icon_url: Optional[str] = None
    color: Optional[int] = None
    thread_id: Optional[str] = None
    monetization_status: Optional[MonetizationStatus] = None
    approved: Optional[datetime] = None
    queued: Optional[datetime] = None
    moderator_message: Optional[object] = None # DEPRECATED
    license: Optional[ProjectLicense] = None 
    versions: Optional[list[str]] = None
    game_versions: Optional[list[str]] = None
    loaders: Optional[list[str]] = None 
    gallery: Optional[GalleryImage] = None

@dataclass
class ProjectResult:
    slug: str
    title: str
    description: str
    client_side: Required
    server_side: Required
    project_type: ProjectType
    downloads: int
    project_id: str
    author: str
    versions: list[str]
    follows: int
    date_created: datetime
    date_modified: datetime
    license: str
    categoriess: Optional[list[str]] = None
    icon_url: Optional[str] = None
    color: Optional[int] = None
    thread_id: Optional[str] = None
    monetization_status: Optional[MonetizationStatus] = None
    display_categories: Optional[list[str]] = None
    latest_version: Optional[str] = None
    gallery: Optional[list[str]] = None
    featured_gallery: Optional[str] = None

@dataclass
class SearchResult:
    slug: str
    title: str
    description: str
    client_side: Required
    server_side: Required
    project_type: ProjectType
    downloads: int
    project_id: str
    author: str
    versions: list[str]
    follows: int
    date_created: datetime
    date_modified: datetime
    license: ProjectLicense
    categories: Optional[list[str]] = None
    icon_url: Optional[str] = None
    color: Optional[int] = None
    thread_id: Optional[str] = None
    monetization_status: Optional[MonetizationStatus] = None
    display_categories: Optional[list[str]] = None
    latest_verssion: Optional[str] = None
    gallery: Optional[str] = None
    featured_gallery: Optional[str] = None

@dataclass
class Version:
    name: str
    version_number: str
    game_versions: list[str]
    version_type: VersionType
    loaders: list[str]
    featured: bool
    id: str
    project_id: str
    author_id: str
    date_published: datetime
    downloads: int
    files: VersionFile
    changelog: Optional[str] = None
    dependencies: Optional[list[VersionDepencency]] = None
    status: Optional[Status] = None
    requested_status: Optional[RequestedStatus] = None

@dataclass
class User:
    username: str
    id: str
    avatar_url: str
    created: datetime
    role: UserRole
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    payout_data: Optional[UserPayoutData] = None
    badges: Optional[UserBadges] = None
    auth_providers: Optional[list[str]] = None
    email_verified: Optional[bool] = None
    has_password: Optional[bool] = None
    has_totp: Optional[bool] = None

@dataclass
class TeamMember:
    team_id: str
    user: User
    role: str
    accepted: bool
    permissions: Optional[TeamMemberPermissions] = None
    payouts_split: Optional[int] = None
    ordering: Optional[int] = None

class Facet(str, Enum):
    """
    These are the most commonly used facet types:
    """
    ProjectType = "project_type"
    Categories = "categories"
    Versions = "versions"
    ClientSide = "client_side"
    ServerSide = "server_side"
    OpenSource = "open_source"
    """
    Several others are also available for use, though these should not be used outside very specific use cases:
    """
    Title = "title"
    Author = "author"
    Follows = "follows"
    ProjectID = "project_id"
    License = "license"
    Downloads = "downloads"
    Color = "color"
    CreatedTimestamp = "created_timestamp"
    ModifiedTimestamp = "modified_timestamp"
    def __lt__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a.value, '<', b))
    def __gt__(a: Self, b: int|str) -> str:
        return(FacetContainer(a.value, '>', b))
    def __le__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a.value, '<=', b))
    def __ge__(a: Self, b: int|str) -> str:
        return(FacetContainer(a.value, '>=', b))
    def __eq__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a.value, ':', b))

@dataclass
class FacetContainer:
    key: Facet
    sign: str
    value: int|str|datetime
    def get(self):
        return(f'"{self.key}{self.sign}{self.value}"')

def facets_to_str(facets: list[list[FacetContainer]]):
    result = ','.join([f'[{','.join([facet.get() for facet in group])}]' for group in facets])
    return result

#facets = [[Facet.Author=='coffeemeow'], [Facet.Versions == '1.20.1', Facet.Versions == '1.20.4']]