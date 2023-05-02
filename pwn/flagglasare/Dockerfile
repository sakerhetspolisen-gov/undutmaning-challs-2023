FROM docker.io/ubuntu:22.10

RUN apt update && apt upgrade -y
RUN apt install dotnet6 xinetd -y

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir -p /home/ctf

COPY Program.cs /home/ctf/
COPY run.sh /home/ctf/
COPY flag.txt /home/ctf/
COPY flagglasare.csproj /home/ctf/
COPY xinetd_config /etc/xinetd.d/

RUN dotnet build /home/ctf -c Release

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/

EXPOSE 1337
CMD xinetd -dontfork
