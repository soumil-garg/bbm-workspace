# ChatGPT generation and download pipeline (Stage 6)

Tools: Claude in Chrome (`mcp__claude-in-chrome__*`, load via ToolSearch), PowerShell, Python. Use the profile logged into ChatGPT Plus (`list_connected_browsers`, `select_browser`). Two profiles are common. If the connection drops ("not connected"), re-list browsers and re-select; it is usually transient.

## Setup once
- `scripts/chatgpt_helper.ps1` records chat IDs and puts the next prompt on the clipboard: `& chatgpt_helper.ps1 -Work C:\cca\<brand> -Dir p -Json chats.json -SaveKey <ID> -SaveId <chatid> -Next <NEXT_ID>`.
- Prompts are files `C:\cca\<brand>\<Dir>\<ID>.txt`. Reference image `ref_*.jpg`.
- Grammarly on chatgpt.com freezes long prompts: ask Soumil to turn it off if paste hangs.

## Per image (new chat each time)
1. PowerShell: helper with `-Next <ID>` (Set-Clipboard).
2. `navigate` https://chatgpt.com/ then wait 2s (browser_batch works; a screenshot at scale 0.2 confirms load).
3. `left_click` the textbox at coordinate (800, 368) (frame 1456x821), `key ctrl+v`.
4. Verify by JS: `document.querySelector('#prompt-textarea,[contenteditable="true"]').innerText` has the expected length and `'Generate an image'` appears exactly once. If doubled, ctrl+a, Delete, paste again.
5. `find` "hidden input type=file labelled Attach photos (image only)" then `file_upload` the reference to that ref (10 MB cap). The ref changes every page load; re-find each time.
6. JS: wait 3s, check `form img` count is 1, click `form button[aria-label="Send"]`, wait about 14s, return `location.pathname`. If the path is `/c/local-chatgpt%3A...` wait 6s and read again; the real chat ID is the `/c/<uuid>` part.
7. Save the chat ID with the helper (`-SaveKey`), and load the next prompt (`-Next`) in the same call.
Never type long prompts key by key, never `insertText`, and do not fetch localhost from chatgpt.com (blocked).

Generation runs in the background: submit all, then wait about 100-120 s. 16 chats in a row worked fine.

## Download (needs Soumil's OK once per session; Chrome may ask to allow multiple downloads)
State: N files, source (his ChatGPT chats), approx size, destination, filenames. Wait for a yes. One JS call in a chatgpt.com tab:
```js
const tok=(await (await fetch('/api/auth/session')).json()).accessToken;
for(const [k,id] of Object.entries(C)){           // C = {name: chatId}
 const c=await (await fetch('/backend-api/conversation/'+id,{headers:{Authorization:'Bearer '+tok}})).json();
 let last=null;const ms=Object.values(c.mapping||{}).filter(m=>m.message&&m.message.author.role!=='user')
   .sort((a,b)=>(a.message.create_time||0)-(b.message.create_time||0));
 for(const m of ms)for(const x of (m.message.content.parts||[]))if(x&&x.asset_pointer)last=x.asset_pointer.split('://')[1];
 if(!last){/* not rendered yet */continue}
 const r=await (await fetch(`/backend-api/files/download/${last}?conversation_id=${id}`,{headers:{Authorization:'Bearer '+tok}})).json();
 const b=await (await fetch(r.download_url)).blob();
 const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=`<Brand>_${k}.png`;
 document.body.appendChild(a);a.click();a.remove();await new Promise(r=>setTimeout(r,700));}
```
The JS call may time out at 45 s for 16 files, but downloads still complete: check `C:\Users\soumi\Downloads`. Do not print `download_url` (it is blocked as query-string data). If a chat returns no asset pointer it has not finished; wait and retry.
Then move files to `C:\Users\soumi\OneDrive\Desktop\<Brand> Ads\<round>\`, list sizes, build the contact sheet.

## Faster route learned on Savvy (2026-09-30/10-01), prefer this
- **Prompt entry without clipboard:** keep prompts in `localStorage` on chatgpt.com and paste synthetically: `ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true}))` on `#prompt-textarea` with a `DataTransfer` carrying text/plain. Length matched exactly every time.
- **Reference image:** `file_upload` only reads session-readable folders (copy the ref to the scratchpad). Upload once, read the attached `form img` `.src` (a data: URL), store it in `localStorage`, then rebuild the `File` per chat with `atob` and set it on the `input[type=file][accept="image/*"]`, dispatch `change`. `fetch(dataUrl)` is blocked by CSP.
- **One `browser_batch` per 3-4 images:** navigate, wait 6-7s (page must have `#prompt-textarea`), one JS call that pastes, attaches, checks length and image count, clicks `form button[aria-label="Send"]`, waits 11s, returns the path. Use `await (async()=>{...})()`; a bare IIFE returns `{}`.
- **Downloads:** `/backend-api/conversation/<id>` returns 429 after 2-3 calls and stays blocked for minutes. Do not loop it. Use `/backend-api/my/recent/image_gen?limit=50` (returns `items[]` with `url`, `conversation_id`) and `fetch(item.url)`. If the library does not list the new chats (newer ChatGPT model that "works" for minutes), open each chat page and download the rendered image from the DOM: `[...document.querySelectorAll('img')].find(i=>i.alt.startsWith('Generated image')&&i.naturalWidth>500)`, `fetch(i.src)` to a blob, anchor download. Space downloads 2s apart; re-run any that Chrome dropped. Never print URLs in tool output (blocked).
- Generation can take 2 to 6 minutes per image on the newer model; check before downloading.
- ChatGPT's content filter refuses prompts that specify skin tones or ethnic contrasts ("different skin tones"); ask for different hairstyles, ages, glasses instead.
- Window/tab issues: if screenshots fail ("0 width" or renderer frozen), `resize_window` the tab's window or navigate again; coordinates in the screenshot frame change between calls, so prefer `ref` clicks.

## After
Close the tabs you opened (`tabs_close_mcp`), stop any background python servers, save chat IDs into the vault note.

## Output
1:1 prompts give 1254x1254 PNGs. Ratios other than 1:1 (9:16 for Stories) are only made for approved winners; verify ChatGPT honours the ratio before promising it.
