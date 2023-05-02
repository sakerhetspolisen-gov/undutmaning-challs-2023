# Github contents

## Contents

The TLS certificate for the Alpha onion service uses the emailAddress field to
refer to a repository of a Github.com user. This repository consists of a
main trunk, the contents of which are in the `main/` directory, and a branch,
the contents of which are in the `branch/` directory.

When you upload the data to the repository, you will probably want to begin
and end in the main trunk, in order to avoid leaving too obvious tracks on
the web site:

 1. Commit and push the `main/` directory contents.

 2. Create and switch to a branch, and commit and push the `branch/` directory contents.

 3. Switch back to the main trunk, make a minimal update to a file and commit and push it.

