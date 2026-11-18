# Thai "กวนตีน" language pack for Hermes Agent: translation guide

You are translating UI strings of Hermes Agent (an AI agent app: CLI, terminal TUI, desktop app)
into Thai, in a playful, cheeky "กวนตีน" tone. The user is Thai and wants the UI to joke around.

## Input / output
- Input: `chunk_NN.en.json`, a flat JSON object `{"<surface>::<dotted.key>": "English text"}`.
  Surface is `core` (CLI/gateway/chat-platform messages), `tui` (terminal UI) or `desktop` (desktop app).
- Output: `chunk_NN.th.json`: the SAME keys (all of them, no extras), values translated to Thai.
  Write valid UTF-8 JSON (`ensure_ascii=False`). Work in batches. Write the batches with Python
  (json.load / json.dump) into the output file, not by hand-editing large JSON. Do not ever print the
  whole file.
- Check: `cd ~/.hermes/cache/scratch/th-update && python3 check.py NN` must print `0 issues`.
  Fix everything it reports and rerun until clean.
- Final answer: one line with the key count and the checker's last line. Nothing else.

## Hard rules (breaking these breaks the app)
1. Keep every placeholder exactly as written, same count: `{name}`, `{count}`, `{0}`, `{1}` ...
   Never translate the text inside braces. Thai word order may move them.
2. Keep leading spaces, `\n` newlines, emoji and symbols (⚠️ ✓ ✗ ⏱ → •), markdown (`**`, backticks),
   URLs, file paths, shell commands, config keys, env vars, CLI flags, slash commands (`/model`),
   key names (Enter, Esc, Tab, Ctrl+C, ↑/↓), and code inside backticks. All unchanged.
3. Brand and product names stay English: Hermes, Nous, Nous Portal, Claude, Anthropic, OpenAI, Codex,
   Telegram, Discord, Slack, LINE, WhatsApp, GitHub, MCP, API, OAuth, YAML, JSON, etc.
4. Input-token lists (keys containing `inputs`, e.g. `"approve,yes,ok,okay,confirm,y"`): keep EVERY
   English token in the same order, and you may APPEND Thai synonyms after a comma
   (e.g. `"approve,yes,ok,okay,confirm,y,ได้,โอเค,จัดไป"`). Never remove an English token.
5. Letter-shortcut prompts like `[o]nce | [s]ession | [d]eny` and `Choice [o/s/D]:` must keep the same
   bracketed letters so typing o/s/a/d still works. Example: `[o] ครั้งเดียว | [s] ทั้งเซสชัน | [d] ไม่ให้`.
6. A value that is purely technical (a unit, `{0}s`, `{0} MB`, a format like `{0}/{1}`, a lone symbol)
   may stay unchanged.
7. Keep length close to the English. Buttons, tabs, menu items and labels must stay SHORT (1-3 words).
   Labels MAY be cheeky: a slangier synonym of about the same length whose action is still obvious
   (บันทึก->เซฟเลย, เริ่ม->ลุย, หยุด->พอก่อน). Tool names are labels: clear Thai (Terminal->เทอร์มินัล,
   Read File->อ่านไฟล์, Patch->แพตช์). Never joke in approvals, billing/cards, keys/credentials,
   delete/reset/uninstall, permissions, input-token lists or shortcuts: exact meaning only.
   Light swearing (แม่ง/เชี่ย) at most once per long description, never on labels, never aimed at the user.
   Put the humour in longer messages, empty states, tips, loaders, success/error messages.

## Tone
- Casual Thai, friend-to-friend, cheeky. Use particles like เว้ย, โว้ย, วะ, นะจ๊ะ, ซะ, หน่อย, ดิ, ล่ะ.
- Mild teasing is fine ("ใจเย็น", "รอแป๊บ กำลังเค้นสมอง", "พังซะแล้ว", "ไม่ให้ทำโว้ย").
  No heavy profanity (no เหี้ย/สัส/ควย), no insults about the user's ability, no emoji added.
- CLARITY FIRST, joke second: for security warnings, dangerous commands, approvals, payments/billing,
  credentials/API keys, data loss, deletion and errors, the meaning must be 100% clear and exact.
  A light teasing tail is OK only if it cannot be misread.
- Do not address the user with a pronoun when you can avoid it. If needed use "มุง" (you) and "กรู" (I,
  the agent), but sparingly; most strings need no pronoun.
- Write Thai numbers as Arabic digits.

## Glossary (use consistently)
session=เซสชัน, agent=เอเจนต์, subagent=ซับเอเจนต์, tool=ทูล, skill=สกิล, plugin=ปลั๊กอิน,
model=โมเดล, provider=ผู้ให้บริการ, gateway=เกตเวย์, profile=โปรไฟล์, settings=ตั้งค่า,
config=คอนฟิก, memory=ความจำ, workspace=เวิร์กสเปซ, project=โปรเจกต์, token=โทเคน, credits=เครดิต,
cron job=งาน cron, webhook=เว็บฮุก, terminal=เทอร์มินัล, prompt=พรอมต์, context=คอนเท็กซ์,
connector=คอนเน็กเตอร์, theme/skin=ธีม, approve=อนุมัติ, deny=ไม่ให้, cancel=ยกเลิก, save=บันทึก,
delete=ลบ, retry=ลองใหม่, loading=กำลังโหลด, error=ข้อผิดพลาด / พัง, sign in=ล็อกอิน,
sign out=ล็อกเอาต์, voice=เสียง, microphone=ไมค์, notification=แจ้งเตือน, file=ไฟล์, folder=โฟลเดอร์.
