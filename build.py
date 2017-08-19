import platform
from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="stable", archs=["x86_64"])
    builder.add_common_builds(shared_option_name="bzip2:shared")

    #TODO(fernando): redundant? check it!
    if platform.system() == "Windows":  # Library not prepared to create a .lib to link with
        # Remove shared builds in Windows
        static_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if not ("bzip2:shared" in options and options["bzip2:shared"]):
                static_builds.append([settings, options, env_vars, build_requires])

        builder.builds = static_builds

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["build_type"] == "Release" \
                and not ("bzip2:shared" in options and options["bzip2:shared"]):
            filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds

    builder.run()
