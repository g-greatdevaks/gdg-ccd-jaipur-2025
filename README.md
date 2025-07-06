# gdg-ccd-jaipur-2025

A repository containing talk material used during Google Cloud Community Day Jaipur 2025 for the talk titled "Serverless Magic: Bringing AI Agents to Life with MCP and Cloud Run".

---

## Author
Anmol Krishan Sachdeva</br>
Sr. Hybrid Cloud Architect, Google</br>
[LinkedIn@greatdevaks](https://www.linkedin.com/in/greatdevaks) | [Twitter@greatdevaks](https://www.twitter.com/greatdevaks)

---

## 📁 mcp-demo

The `mcp-demo` directory contains a hands-on demo project for building and connecting **MCP Servers** and **MCP Clients** using [FastMCP](https://gofastmcp.com/), supporting both local and remote (cloud) deployments.

This project features:
- **Math operations** and **number-in-words explanations** powered by Gemini LLM (leveraging Sampling handler pattern).
- A **Streamlit Web Application** for interactive exploration.
- A **CLI-based MCP Client** for command-line testing.
- A **serverless barcode generator tool** hosted on Google Cloud Run as a remote MCP Server.

The demo showcases how to compose and orchestrate tools across local and remote MCP servers, enabling hybrid LLM agent workflows.

For complete instructions and setup, see: [`mcp-demo/README.md`](./mcp-demo/README.md).

---

## Disclaimer
- The content and views presented during the session are author’s own and not of any organizations they are associated with.
- Some images used in this presentation were generated with the assistance of artificial intelligence. Such illustrative representations may not convey accurate or factually correct information.
- **The code shown in this repository is for illustration and educational purposes only.**
    - Not production-grade; error handling, security, and scalability are not fully addressed.