Instructions to build a Docker and run Pathway Tools (Unix Only).
-----------------------------------------------------------------

The Pathway Tools software comes with a Lisp interpreter outdated and working only on Ubuntu 16.04.

If you ran into the following error:

```
An unhandled error occurred during initialization:
Loading sys:aclssl.so failed with error:
/opt/pathway-tools/aic-export/pathway-tools/ptools/24/exe/aclssl.so: undefined symbol: CRYPTO_set_locking_callback.
```

Please do:

1. **Edit the Dockerfile**: Change `/opt/pathway-tools/pathway-tools` with the complete path to the pathwaytools executable.

2. **Build the docker**: In a terminal, execute `docker build . --tag ptools-v24` (change the tag accordingly)

3. **Run the docker**: In a terminal, execute `docker run --detach --network host --rm --volume /opt:/opt ptools-v24`
   (employ the tag and change the volume path accordingly to match the base installation directory)

Argument          | Explanation:
------------------|--------------------------------------------------------
--detach          | Run container in background and print container ID
--rm              | Automatically remove the container when it exits
--network network | Connect a container to a network
--volume list     | Bind mount a volume
