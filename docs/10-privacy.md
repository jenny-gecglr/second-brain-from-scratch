# 10. Privacy: what stays out, what stays inside

A second brain concentrates everything about you in one folder. Decide the boundaries on day one.

## Three levels
```yaml
privacy: open       # or no field at all: work knowledge, rules, tool notes
privacy: internal   # your own business, legal or financial matters
privacy: private    # personal, family, health, money, other people's information
```
| Level | Agents and outside tools |
|---|---|
| open | usable by any agent or tool |
| internal | used only inside your own session when you ask; not bulk-given to a sub-agent or shared |
| private | read only when you open it on purpose; never given to a sub-agent or outside tool unless you say so |

## It is a convention, not a lock
An agent running in your folder can open any file if you let it. The field only tells agents and scripts how to behave. For real secrecy, keep the file **outside the vault**. The doctor warns when an imported chat note has no `privacy:` field.

## Never in the vault
Passwords, recovery codes, API keys and tokens, ID and visa documents, bank or credit data. If such a file shows up in an import list, the agent says "never imported" and moves on.

## Names and sensitive facts in notes
- Decide whether a former employer's name may appear in your notes. If not, write it once in `AGENTS.md` as a rule ("describe past jobs without company names") and tell sub-agents the same in their brief (write "employer", not the name).
- Personal figures (salary, bonus, debt) stay in `private` pages, not in rules or summaries.
- An analysis of your own work reports can be written without numbers; keep a clearly marked "numbers" section for the places where figures belong (for example a CV).

## Sending notes to outside tools
Before giving anything to an outside model or service (including a sub-agent running in another vendor's tool), check the `privacy:` field and your scope decisions. Private notes are not sent unless you say so.

## Sharing this vault or a repo built from it
Never publish the vault. For a public template, start from a clean copy, remove everything personal, and run a mechanical scan (see the README, "Publishing your own version"). Read it yourself before it goes public.
