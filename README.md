# Tatar Path

> **Concept only — there is no code in this repository yet.**
> This repo holds a design document that is meant to be argued with and sharpened.

**BloodHound tells you every path. Tatar Path tells you where to start.**

[**→ Read the concept document**](docs/concept.html) *(open the file in a browser; it is a
self-contained page with no dependencies)*

---

## The idea in one paragraph

On a red team engagement, SharpHound collects and BloodHound draws hundreds of attack
paths. That is a map, not a decision. BloodHound ranks by hop count, which says nothing
about how hard, how loud, or how reliable a step actually is, and it has no notion of
what the operator currently owns. Tatar Path is a **triage layer** on top of the data
that is already there: it reads the graph, weights each edge by real exploitability —
effort, noise, reliability, impact — finds the cheapest path from the set you already
control, and prints a ranked "start here" list with ready-to-run commands filled in
with the environment's real object names, plus an OpSec note per step.

It does not collect (SharpHound does that) and it does not store (Neo4j does that).
It adds the reasoning and output layer, which is the part that is missing.

## Status

| | |
|---|---|
| **Stage** | Concept / design draft |
| **Code** | None yet |
| **Document** | [`docs/concept.html`](docs/concept.html) |
| **Intended stack** | Python + the neo4j driver; local Ollama for the optional reasoner |
| **Licence** | MIT |

The document's own roadmap sketches v0.1 (CLI triage) → v0.2 (owned-aware next best
action) → v0.3 (offline Ollama reasoner) → v1.0 (Tatar ecosystem integration).

## Scope and authorisation

Tatar Path is **offensive tooling**. The design is explicit that it is a triage layer
and not an exploitation tool: it prints ranked candidates and prepared commands, and a
human reviews and runs them. It never executes anything itself, and the "owned" set is
asserted by the operator — the tool does not acquire or verify it.

Use only within an engagement you have **written authorisation** for. The sample
commands in the document use placeholder names (`dc01`, `corp.local`, `-p '***'`).

## Where this sits

Each Tatar tool answers one question:

| | You already have | Tatar tells you |
|---|---|---|
| Tatar-Triage | Logs on a host | what to look at |
| Tatar-Kuber | Findings from K8s scanners | what to trust |
| **Tatar-Path** | **Attack paths from BloodHound** | **where to start** |
| Tatar-Flow | HTTP requests in a proxy | what to test, in what context |
| Tatar-Relay | An encrypted/signed protocol | how to talk to it |

## Feedback

The document is a draft meant to be sharpened by discussion. Disagreement about the
edge-weighting model, the ranking, or the scope is the most useful kind of feedback.

---

<h2 id="mongol">Монгол хэл дээр</h2>

> **Зөвхөн концепц — энэ репод код хараахан байхгүй.**
> Энд байгаа нь хэлэлцэн хурцлах зорилготой дизайн ноорог.

**BloodHound бүх замыг харуулна. Tatar Path хаанаас эхлэхийг хэлж өгнө.**

[**→ Концепцийн баримтыг унших**](docs/concept.html) *(хөтчөөр нээнэ — гадны хамааралгүй,
бүтэн нэг хуудас)*

### Санаа нэг догол мөрөөр

Улаан багийн ажлын үед SharpHound цуглуулж, BloodHound олон зуун довтолгооны замыг
зурдаг. Энэ бол зураглал болохоос шийдвэр биш. BloodHound үсрэлтийн тоогоор эрэмбэлдэг
ч тухайн алхам бодитоор хэр хялбар, хэр чимээтэй, хэр найдвартай болохыг тооцдоггүй,
мөн операторын одоо эзэмшиж байгаа зүйлийг мэддэггүй. Tatar Path нь аль хэдийн байгаа
өгөгдөл дээр суусан **triage давхарга**: графыг уншиж, ирмэг бүрийг бодит
exploitability-ээр — хүчин чармайлт, чимээ, найдвар, нөлөө — жинлээд, эзэмшсэн
олонлогоос хамгийн бага зардлын замыг олж, тухайн орчны бодит объектын нэрсээр
бөглөсөн бэлэн командтай, алхам бүрдээ OpSec тэмдэглэлтэй «эхлэх цэг»-ийн эрэмбэтэй
жагсаалтыг хэвлэнэ.

Цуглуулга (SharpHound), хадгалалт (Neo4j)-ыг дахин зохиохгүй. Дутуу байгаа хэсэг болох
reasoning ба гаралтын давхаргыг л нэмнэ.

### Төлөв

| | |
|---|---|
| **Үе шат** | Концепц / дизайн ноорог |
| **Код** | Хараахан байхгүй |
| **Баримт** | [`docs/concept.html`](docs/concept.html) |
| **Төлөвлөж буй стек** | Python + neo4j driver; сонголтот reasoner-т локал Ollama |
| **Лиценз** | MIT |

Баримтын замын зураг: v0.1 (CLI triage) → v0.2 (эзэмшсэнд тулгуурласан дараагийн алхам)
→ v0.3 (офлайн Ollama reasoner) → v1.0 (Tatar экосистемтэй нэгдэх).

### Хүрээ ба зөвшөөрөл

Tatar Path бол **довтолгооны хэрэгсэл**. Дизайн нь үүнийг triage давхарга гэж тодорхой
заасан — exploitation хэрэгсэл биш: эрэмбэлсэн саналууд ба бэлтгэсэн командыг хэвлэх
бөгөөд хүн хянаж гүйцэтгэнэ. Өөрөө юу ч ажиллуулахгүй, «эзэмшсэн» олонлогыг оператор
өөрөө мэдүүлнэ — хэрэгсэл түүнийг олж авахгүй, шалгахгүй.

Зөвхөн **бичгээр зөвшөөрөгдсөн** engagement-ийн хүрээнд хэрэглэнэ. Баримт дахь жишээ
командууд нь орлуулагч нэр (`dc01`, `corp.local`, `-p '***'`) ашигласан болно.

### Экосистем дэх байрлал

Tatar хэрэгсэл бүр нэг асуултад хариулна:

| | Чамд бэлэн байгаа | Tatar хэлж өгнө |
|---|---|---|
| Tatar-Triage | Хост дээрх лог | юу харах вэ |
| Tatar-Kuber | K8s scanner-ийн finding | юунд итгэх вэ |
| **Tatar-Path** | **BloodHound-ийн attack path** | **алинаас эхлэх вэ** |
| Tatar-Flow | Proxy дээрх HTTP request | ямар функцийг ямар контекстээр тестлэх вэ |
| Tatar-Relay | Шифрлэгдсэн/гарын үсэгтэй протокол | хэрхэн харилцах вэ |

### Санал хүсэлт

Баримт бол хэлэлцэн хурцлах зорилготой ноорог. Ирмэгийн жинлэлтийн загвар, эрэмбэлэлт,
хамрах хүрээний талаарх эсрэг санал хамгийн их хэрэгтэй.
