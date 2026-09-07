# Documentação de Skills do Manguito GitHub

Este diretório contém as especificações completas das **skills** consumidas pela inteligência do bot **Manguito GitHub** (`services/gemini_service.py`). 

Em tempo de execução, o bot carrega dinamicamente o conteúdo na íntegra destas skills e as injeta no `system_instruction` do modelo **`gemini-3.5-flash`**.

---

## 📚 Skills Utilizadas

### 1. `humanizer` ([`humanizer.md`](./humanizer.md))
* **Propósito**: Remove vícios de escrita típicos de modelos de IA (ex: *"revolucionário"*, *"testemunho de"*, *"focal point"*, intros e fechamentos robóticos). Força uma escrita em português fluida, direta e natural.
* **Origem**: Baseado no guia comunitário [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup) e mantido pelo ecossistema Antigravity/Claude Code (`@blader`).

---

### 2. `release-notes` ([`release-notes.md`](./release-notes.md))
* **Propósito**: Orienta a transformação de logs brutos de commits e PRs do Git em **Release Notes Executivas** focadas no valor ao usuário/negócio. Define a categorização padrão (Novas Funcionalidades, Melhorias, Bugs, Atenção).
* **Origem**: Skill padrão de engenharia de produto do ecossistema Antigravity PM Toolkit.

---

### 3. `commit-work` ([`commit-work.md`](./commit-work.md))
* **Propósito**: Define a taxonomia de Conventional Commits (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`) permitindo ao bot decodificar mensagens de commit breves com precisão técnica.
* **Origem**: Especificação comunitária [Conventional Commits](https://www.conventionalcommits.org/).

---

### 4. `pre-mortem` ([`pre-mortem.md`](./pre-mortem.md))
* **Propósito**: Análise preditiva de riscos categorizando ameaças em **Tigers** (riscos reais), **Paper Tigers** (falsos alertas) e **Elephants** (questões veladas).
* **Origem**: Metodologia de gestão de risco de produto utilizada na Meta / Instagram e documentada no Product Compass.

---

### 5. `create-prd` ([`create-prd.md`](./create-prd.md))
* **Propósito**: Define o modelo de especificação de produtos (8 seções) utilizado para criar a documentação oficial da automação (MANGUEHOU-8) no Mangue Point para o PM Eduardo Gois.
* **Origem**: Inspirado no template oficial de PRD do Product Compass / OpenAI (Miqdad Jaffer).

---

## 🔄 Como o Python consome estas skills

O módulo `services/gemini_service.py` lê os arquivos Markdown deste diretório no momento da geração do relatório e concatena seus conteúdos na instrução do modelo Gemini:

```python
def load_skill(filename: str) -> str:
    path = os.path.join("skills", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
```
