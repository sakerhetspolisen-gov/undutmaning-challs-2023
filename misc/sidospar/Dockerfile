FROM docker.io/rust:latest AS compile
COPY . /work
WORKDIR /work
RUN cargo build --release

FROM docker.io/debian:bullseye-slim
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir -p /home/ctf
COPY --from=compile /work/target/x86_64-unknown-linux-gnu/release/challenge /home/ctf/challenge
RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/
EXPOSE 2323
CMD /home/ctf/challenge
