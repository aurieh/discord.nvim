import cffi
from os.path import basename, exists, join
from os import environ as env
from time import time


DISCORD_DEF = """
typedef struct DiscordRichPresence {
    const char* state;   /* max 128 bytes */
    const char* details; /* max 128 bytes */
    int64_t startTimestamp;
    int64_t endTimestamp;
    const char* largeImageKey;  /* max 32 bytes */
    const char* largeImageText; /* max 128 bytes */
    const char* smallImageKey;  /* max 32 bytes */
    const char* smallImageText; /* max 128 bytes */
    const char* partyId;        /* max 128 bytes */
    int partySize;
    int partyMax;
    const char* matchSecret;    /* max 128 bytes */
    const char* joinSecret;     /* max 128 bytes */
    const char* spectateSecret; /* max 128 bytes */
    int8_t instance;
} DiscordRichPresence;
typedef struct DiscordJoinRequest {
    const char* userId;
    const char* username;
    const char* avatar;
} DiscordJoinRequest;
typedef struct DiscordEventHandlers {
    void (*ready)();
    void (*disconnected)(int errorCode, const char* message);
    void (*errored)(int errorCode, const char* message);
    void (*joinGame)(const char* joinSecret);
    void (*spectateGame)(const char* spectateSecret);
    void (*joinRequest)(const DiscordJoinRequest* request);
} DiscordEventHandlers;
void Discord_Initialize(
    const char* applicationId,
    DiscordEventHandlers* handlers,
    int autoRegister,
    const char* optionalSteamId);
void Discord_Shutdown(void);
void Discord_RunCallbacks(void);
void Discord_UpdatePresence(const DiscordRichPresence* presence);
void Discord_Respond(const char* userid, int reply);
"""


class Discord(object):
    def __init__(self, appid):
        self.ffi = cffi.FFI()
        self.ffi.cdef(DISCORD_DEF)
        self.libfile = None
        paths = ["/usr/lib/", "/lib", join(env.get("HOME"), ".local/lib/")]
        for path in paths:
            path = join(path, "libdiscord-rpc.so")
            if exists(path):
                self.libfile = path
        if not self.libfile:
            raise Exception(
                "Couldn't locate libdiscord-rpc.so, searched in {}".format(
                    ", ".join(paths)
                )
            )
        self.lib = self.ffi.dlopen(self.libfile)
        self.lib.Discord_Initialize(
            appid,
            self.ffi.NULL, 0, b"",
        )

    def update_presence(self, filename, filetype):
        presence_payload = {}
        presence_payload["details"] = self.ffi.new(
            "char[]", bytes("Editing {}".format(basename(filename)), "utf8")
        )
        presence_payload["largeImageKey"] = self.ffi.new("char[]", b"neovim")
        presence_payload["largeImageText"] = self.ffi.new(
            "char[]", b"The One True Editor"
        )
        presence_payload["startTimestamp"] = int(time())
        # FIXME: Refactor
        if len(filetype) > 0:
            presence_payload["smallImageKey"] = self.ffi.new(
                "char[]", bytes(filetype, "us-ascii")
            )
            presence_payload["smallImageText"] = self.ffi.new(
                "char[]", bytes(filetype, "us-ascii")
            )
        self.lib.Discord_UpdatePresence(
            self.ffi.new("DiscordRichPresence*", presence_payload)
        )

    def shutdown(self):
        self.lib.Discord_Shutdown()

    def __del__(self):
        self.lib.Discord_Shutdown()
