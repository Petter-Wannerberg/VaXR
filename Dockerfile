FROM ghcr.io/epicgames/unreal-engine:dev-5.3.1 as builder

# Copy the source code for the project into the container
COPY --chown=ue4:ue4 . /tmp/project

# Build and package the dedicated server for the project
RUN /home/ue4/UnrealEngine/Engine/Build/BatchFiles/RunUAT.sh BuildCookRun \
        -Server -NoClient -ServerConfig=Development \
        -Project=/tmp/project/VAXR_Lab.uproject \
        -UTF8Output -AllMaps -NoP4 -Build -Cook -Stage -Pak -Package -Archive \
        -ArchiveDirectory=/tmp/project/Packaged \
        -Platform=Linux

# Copy the packaged files into a minimal container image
FROM gcr.io/distroless/cc-debian12:nonroot
#FROM debian:bookworm
COPY --from=builder --chown=nonroot:nonroot /tmp/project/Packaged/LinuxServer /home/nonroot/project

# Expose the port that the dedicated server listens on
EXPOSE 7777/udp

# Set the dedicated server as the container's entrypoint
ENTRYPOINT ["/home/nonroot/project/VAXR_Lab/Binaries/Linux/VRExpPluginExampleServer"]