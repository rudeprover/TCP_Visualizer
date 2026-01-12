# TCP Handshake Visualizer

This project is a small educational application that demonstrates how a real
TCP connection is created using the standard socket API, and how that process
maps to the TCP handshake you see in tools like Wireshark.

The goal is to connect **socket programming**, **TCP theory**, and **OS behavior**
without using packet sniffing or special privileges.

---

## What This Program Does

- Creates a real TCP socket using `socket()`
- Initiates a real TCP connection using `connect()`
- Displays inferred TCP states in a Tkinter GUI
- Runs entirely in user space
- Requires no root or administrator privileges

The program does **not** capture packets. It visualizes TCP behavior the same
way real applications experience it: through socket API calls and their
outcomes.

---

## What This Program Does NOT Do

- Does not sniff or inspect packets
- Does not use raw sockets
- Does not bypass the kernel TCP stack
- Does not require elevated privileges

If you want to see raw SYN / ACK packets, use Wireshark or tcpdump instead.

---

## How TCP Is Observed Here

Applications never see TCP packets directly. They observe TCP indirectly:

| Application Call | Kernel TCP Action            |
|------------------|------------------------------|
| `socket()`       | Allocate kernel socket       |
| `connect()`      | Send SYN, wait for handshake |
| return from `connect()` | Handshake complete    |
| `close()`        | Send FIN / teardown          |

The GUI shows these inferred states explicitly.

---

## Visualized States

| Displayed State | Meaning |
|-----------------|--------|
| CLOSED | No socket exists |
| SOCKET CREATED | Kernel socket allocated |
| SYN-SENT | `connect()` in progress |
| ESTABLISHED | TCP handshake complete |
| CLOSED | Socket closed |

`SYN-RECEIVED` is a server-side state and is not directly observable by a client.

---

## Requirements

- Python 3.8 or newer
- Tkinter (included with most Python distributions)

To verify Tkinter is available:

```bash
python -m tkinter
