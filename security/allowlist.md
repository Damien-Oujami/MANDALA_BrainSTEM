# 🔐 Security Domain Allowlist

This document records **why** each external domain is allowed for builds, deployments, and Codex-assisted automation.  
The allowlist prevents CI/CD pipelines from stalling on missing package mirrors while keeping our network surface intentional.  

---

## 🧩 How it works
- **CI jobs & Codex**: When GitHub Actions (or Codex) runs `pip install`, `npm install`, `cargo build`, `docker pull`, etc., the runner must fetch packages from official registries.  
- **Allowlist**: These domains are explicitly permitted. Any request outside this set is denied.  
- **Updates**: If a build fails with “could not resolve host,” check the logs, confirm the domain is legitimate, then add it here.  
- **Tracking**: Each entry has a short *reason* and *first-seen date*. This way, nothing sneaks in without context.  

---

## 📦 Package Managers

- **Python**  
  - `pypi.org`, `pypa.io`, `pythonhosted.org`, `pypi.python.org` → Python packages  
- **Node.js**  
  - `npmjs.com`, `npmjs.org`, `nodejs.org`, `yarnpkg.com` → Node packages, runtime & Yarn  
- **Rust**  
  - `crates.io`, `rustup.rs` → Rust crates & toolchain  
- **Go**  
  - `golang.org`, `go.dev`, `pkg.go.dev`, `goproxy.io`, `sum.golang.org` → Go modules (proxy + sum + docs)  
- **Ruby**  
  - `rubygems.org`, `ruby-lang.org`, `rubyforge.org`, `rubyonrails.org`, `rvm.io` → Ruby gems and runtime  
- **Java / JVM**  
  - `maven.org`, `repo.maven.apache.org`, `repo1.maven.org`, `jcenter.bintray.com`, `gradle.org`, `services.gradle.org` → Maven/Gradle packages  
  - `java.com`, `java.net`, `oracle.com` → Java runtime  
- **Swift**  
  - `swift.org` → Swift toolchains  
- **Haskell**  
  - `haskell.org`, `hackage.haskell.org` → Haskell packages  
- **PHP**  
  - `packagist.org` → Composer packages  
- **Dart/Flutter**  
  - `pub.dev` → Dart packages  

---

## 🐧 Linux Distros & Repos

- **Ubuntu/Debian**: `debian.org`, `archive.ubuntu.com`, `security.ubuntu.com`, `deb.debian.org`, `security.debian.org`  
- **Alpine**: `alpinelinux.org`, `dl-cdn.alpinelinux.org`  
- **Fedora/CentOS**: `fedoraproject.org`, `centos.org`  
- **Arch**: `archlinux.org`  
- **Launchpad PPAs**: `launchpad.net`, `ppa.launchpad.net`  

---

## 📦 Container Registries

- **Docker**: `docker.com`, `docker.io`, `registry-1.docker.io`, `index.docker.io`  
- **GHCR**: `ghcr.io`  
- **GCR**: `gcr.io`  
- **Quay**: `quay.io`  
- **Azure MCR**: `mcr.microsoft.com`  

---

## 🌐 Code Hosts

- `github.com`, `githubusercontent.com`, `raw.githubusercontent.com`, `objects.githubusercontent.com` → Source pulls, releases, LFS  
- `gitlab.com`, `bitbucket.org` → Additional repos  
- `apache.org`, `sourceforge.net`, `eclipse.org` → Legacy project mirrors  

---

## 🛠 Other Services

- `hashicorp.com` → Terraform & Vault  
- `json-schema.org`, `json.schemastore.org` → Schema validation  
- `packagecloud.io` → Misc. binary packages  
- `bower.io` → Legacy JS packages  

---

## 🧭 Project-Specific (Future/Active)

- `supabase.com`, `supabase.co` → BrainSTEM + Tekita DB integration  
- `n8n.io` → Workflow automation  
- `vercel.com`, `netlify.com` → Landing page hosting  
- `cloudflare.com`, `workers.dev`, `r2.cloudflarestorage.com` → CDN, Workers, R2 storage  

---

## 📜 Change Log

| Date       | Domain(s) Added | Reason | By |
|------------|-----------------|--------|----|
| 2025-08-24 | full baseline   | Initial allowlist for BrainSTEM + tentacle repos | Damien |

---

🔑 **Rule of thumb:** Only add when a build actually fails on a domain. Never add “just in case.” This keeps our net surface minimal but functional.  
