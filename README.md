# Node-Vuln — Vulnerable Node.js Examples, CVEs & Unsafe Patterns

A curated collection of **intentionally vulnerable Node.js/JavaScript code** for learning, research, and defensive testing.
This repository contains vulnerable source code, reproduction snippets, and my analysis of common insecure patterns and libraries used in Node.js/JavaScript ecosystems.


## ⚠️ Important disclaimer (read first)

* **This repository intentionally contains vulnerable code.** It is **only** for educational, research, or defensive testing purposes (CTF, lab exercises, learning secure coding, red-team/blue-team practice).
* **I only provide source code.** Executing any code in this repository is the sole responsibility of the user.
* **Do NOT run these projects on production systems or machines with sensitive data.** Use isolated, disposable environments (VMs, containers, sandbox networks).
* **Legal & ethical notice:** Always get express permission before testing systems you do not own. Misuse may be illegal and unethical.



## Project goals

* Collect real-world vulnerable Node.js examples and insecure JS patterns in one place.
* Document CVEs and practical PoCs that illustrate exploit mechanics.
* Provide short analyses and mitigation strategies for each vulnerability/pattern.
* Link to relevant vulnerable lab environments (e.g., VulnHub labs) used during research so you can reproduce safely.


## Typical vulnerabilities & patterns covered

Examples of the classes of vulnerabilities and unsafe patterns you will find documented here

* Remote Code Execution (RCE) 
* Prototype Pollution
* Insecure DeSerialization
* Server-Side Request Forgery (SSRF)
* Path Traversal / Arbitrary File Read
* Insecure use of third-party packages 


## How the repo is organized

```
├─ CVE-2017-16082 (VulnHub)
|
├─ CVE-2017-14849 (VulnHub)
|
├─ RCE - SSTI/
│  ├─ RCE - SSTI .js
│  ├─ README.md
└─ README.md
```