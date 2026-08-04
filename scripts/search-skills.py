#!/usr/bin/env python3
"""Search the repository Skill discovery index without installing a Skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import NamedTuple


TOKEN_RE = re.compile(
    r"(?:[a-z0-9][a-z0-9.+#-]*|[\u3400-\u4dbf\u4e00-\u9fff]+)",
    re.IGNORECASE,
)
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
DELIVERY_ACTION_RE = re.compile(
    r"\b(?:stage|staged|staging|commit|committed|committing|push|pushed|pushing|"
    r"merge|merged|merging|rebase|rebased|rebasing|tag|tagged|tagging|release|"
    r"released|releasing|publish|published|publishing|cleanup|clean\s+up|cleaned\s+up|cleaning\s+up|"
    r"delete|deleted|deleting|sync|synced|syncing|integrate|integrated|integrating|"
    r"deliver|delivered|delivering|squash|squashed|squashing|resolve|resolved|resolving|"
    r"continue|continued|continuing|checkpoint|checkpointed|checkpointing|"
    r"normalize|normalized|normalizing|pull|pulled|pulling|fetch|fetched|fetching|"
    r"fast-forward|fast forward|fast-forwarded|fast-forwarding|cherry-pick|cherry pick|cherry-picked|cherry-picking|"
    r"abort|aborted|aborting|switch|switched|switching|checkout|checked out|checking out|"
    r"reset|resetting|revert|reverted|reverting|restore|restored|restoring|branch|add|added|adding|rm|clean|cleaned|cleaning)\b",
    re.IGNORECASE,
)
BASE_DELIVERY_ACTIONS = {
    "stage",
    "commit",
    "push",
    "merge",
    "rebase",
    "tag",
    "release",
    "publish",
    "cleanup",
    "delete",
    "sync",
    "integrate",
    "deliver",
    "squash",
    "resolve",
    "continue",
    "checkpoint",
    "normalize",
    "pull",
    "fetch",
    "fast-forward",
    "fast forward",
    "cherry-pick",
    "cherry pick",
    "abort",
    "switch",
    "checkout",
    "reset",
    "revert",
    "restore",
    "branch",
    "add",
    "rm",
    "clean",
}
ACTION_CANONICAL = {
    "stage": "stage", "staged": "stage", "staging": "stage",
    "commit": "commit", "committed": "commit", "committing": "commit",
    "push": "push", "pushed": "push", "pushing": "push",
    "merge": "merge", "merged": "merge", "merging": "merge",
    "rebase": "rebase", "rebased": "rebase", "rebasing": "rebase",
    "tag": "tag", "tagged": "tag", "tagging": "tag",
    "release": "release", "released": "release", "releasing": "release",
    "publish": "publish", "published": "publish", "publishing": "publish",
    "cleanup": "cleanup", "clean up": "cleanup", "cleaned up": "cleanup", "cleaning up": "cleanup",
    "delete": "delete", "deleted": "delete", "deleting": "delete",
    "sync": "sync", "synced": "sync", "syncing": "sync",
    "integrate": "integrate", "integrated": "integrate", "integrating": "integrate",
    "deliver": "deliver", "delivered": "deliver", "delivering": "deliver",
    "squash": "squash", "squashed": "squash", "squashing": "squash",
    "resolve": "resolve", "resolved": "resolve", "resolving": "resolve",
    "continue": "continue", "continued": "continue", "continuing": "continue",
    "checkpoint": "checkpoint", "checkpointed": "checkpoint", "checkpointing": "checkpoint",
    "normalize": "normalize", "normalized": "normalize", "normalizing": "normalize",
    "pull": "pull", "pulled": "pull", "pulling": "pull",
    "fetch": "fetch", "fetched": "fetch", "fetching": "fetch",
    "fast-forward": "fast-forward", "fast-forwarded": "fast-forward", "fast-forwarding": "fast-forward",
    "fast forward": "fast-forward",
    "cherry-pick": "cherry-pick", "cherry-picked": "cherry-pick", "cherry-picking": "cherry-pick",
    "cherry pick": "cherry-pick",
    "abort": "abort", "aborted": "abort", "aborting": "abort",
    "switch": "switch", "switched": "switch", "switching": "switch",
    "checkout": "checkout", "checked out": "checkout", "checking out": "checkout",
    "reset": "reset", "resetting": "reset", "revert": "revert", "reverted": "revert", "reverting": "revert",
    "restore": "restore", "restored": "restore", "restoring": "restore", "branch": "branch",
    "add": "add", "added": "add", "adding": "add", "rm": "rm",
    "clean": "clean", "cleaned": "clean", "cleaning": "clean",
}
GLOBAL_DELIVERY_FORBIDDEN_RE = re.compile(
    r"\b(?:do\s+not\s+(?:(?:make|perform)\s+(?:any\s+)?git\s+changes?|(?:change|modify)\s+git\s+state)|git\s+"
    r"(?:mutation(?:s)?|delivery|operations?|writes|state\s+changes?)\s+(?:is|are)?\s*"
    r"(?:forbidden|prohibited|not\s+allowed))\b",
    re.IGNORECASE,
)
CHINESE_DELIVERY_ACTION_RE = re.compile(r"暂存|提交|推送|合并|变基|打标签|发布|清理")
CHINESE_NEGATION = ("不要", "禁止", "不得", "不可", "不许", "勿", "不允许", "不被允许", "未获授权", "未授权", "待定")
PREFIX_DENIAL_RE = re.compile(
    r"\b(?:do\s+not|don't|never|must\s+not|may\s+not|cannot|can't|without|no)\b|"
    r"\b(?:not\s+(?:[a-z]+\s+){0,2}(?:authorized|permitted|allowed|ready|approved)|"
    r"unauthorized)\b",
    re.IGNORECASE,
)
POSTFIX_DENIAL_RE = re.compile(
    r"\b(?P<verb>is|are|was|were|isn't|aren't|wasn't|weren't|has\s+been|have\s+been)?\s*(?:forbidden|prohibited|revoked|withdrawn|"
    r"not\s+(?:[a-z]+\s+){0,2}(?:allowed|permitted|authorized|ready|approved)|unauthorized)\b",
    re.IGNORECASE,
)
REVOCATION_RE = re.compile(
    r"\b(?:that\s+)?(?:permission|authorization|authority)\s+(?:(?:is|was|has\s+been|have\s+been)\s+)?"
    r"(?:revoked|withdrawn)\b|\b(?:i\s+)?revoke\s+(?:that\s+)?(?:permission|authorization|authority)\b|"
    r"\bscratch\s+that\b",
    re.IGNORECASE,
)
DELIVERY_DIAGNOSTIC_RE = re.compile(
    r"\bnon-fast-forward\b.{0,120}\b(?:inspect|check|report|tell|safe\s+(?:delivery\s+)?path)\b|"
    r"\b(?:inspect|check|report|tell)\b.{0,120}\bnon-fast-forward\b|"
    r"\b(?:git|ref|upstream|origin)\b.{0,80}\bdiverg(?:ed|ence)\b.{0,120}"
    r"\b(?:inspect|check|report|tell|safe\s+(?:delivery\s+)?path)\b|"
    r"\bdiverg(?:ed|ence)\b.{0,80}\b(?:git|ref|upstream|origin)\b.{0,120}"
    r"\b(?:inspect|check|report|tell|safe\s+(?:delivery\s+)?path)\b",
    re.IGNORECASE,
)
DIAGNOSTIC_DENIAL_RE = re.compile(
    r"\b(?:do\s+not|don't|never|must\s+not|may\s+not|cannot|can't)\s+"
    r"(?:inspect|check|report|tell)\b|\b(?:advise|advice)\b",
    re.IGNORECASE,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_index(root: Path) -> dict[str, object]:
    return json.loads((root / "skills-index.json").read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return " ".join(
        token
        for token in TOKEN_RE.findall(value.lower().replace("-", " "))
        if token not in STOP_WORDS
    )


def contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", value))


def canonical_action(action: re.Match[str]) -> str:
    return ACTION_CANONICAL[" ".join(action.group(0).lower().split())]


def targeted_revocation_action(value: str) -> str | None:
    """Resolve either permission-word order for every canonical delivery action."""
    for form, canonical in sorted(ACTION_CANONICAL.items(), key=lambda item: -len(item[0])):
        escaped = re.escape(form)
        if re.search(
            r"\b(?:" + escaped + r")\s+(?:permission|authorization)\b|"
            r"\b(?:permission|authorization)\s+to\s+(?:" + escaped + r")\b",
            value,
            re.IGNORECASE,
        ):
            return canonical
    return None


def is_bare_revocation(revoke_match: re.Match[str], segment: str) -> bool:
    """Whether a revocation withdraws all delivery authority, not another domain's."""
    text = re.sub(
        r"^(?:(?:but|then|and|however|also|therefore|thus|hence|moreover|furthermore|"
        r"nevertheless|nonetheless|consequently|additionally)\s+|(?:please\s+)?note(?:\s+that)?\s+)+",
        "",
        revoke_match.group(0).strip(),
        flags=re.IGNORECASE,
    )
    if re.fullmatch(r"(?:i\s+)?revoke\s+(?:that\s+)?(?:permission|authorization|authority)", text, re.IGNORECASE):
        return True
    if re.fullmatch(r"scratch\s+that", text, re.IGNORECASE):
        return True
    if re.fullmatch(r"授权已撤回|我撤回授权|取消授权|撤销授权", text):
        return True
    if re.fullmatch(
        r"that\s+(?:permission|authorization|authority)\s+"
        r"(?:(?:is|was|has\s+been|have\s+been)\s+)?(?:revoked|withdrawn)",
        text,
        re.IGNORECASE,
    ):
        return True
    if re.search(r"\bto\b", text, re.IGNORECASE):
        return False
    permission = re.search(r"\b(?:permission|authorization|authority)\b", revoke_match.group(0), re.IGNORECASE)
    if permission is None:
        return False
    permission_start = revoke_match.start() + permission.start()
    prefix = segment[:permission_start]
    clause_prefix = re.split(r"[,;:：!?。；]|\.(?=\s|$)|\s[-–—]\s", prefix)[-1].strip()
    clause_prefix = re.sub(
        r"^(?:(?:but|then|and|however|also|therefore|thus|hence|moreover|furthermore|"
        r"nevertheless|nonetheless|consequently|additionally)(?:\s+|$)|"
        r"(?:please\s+)?note(?:\s+that)?(?:\s+|$))+",
        "",
        clause_prefix,
        flags=re.IGNORECASE,
    )
    clause_prefix = re.sub(r"^(?:the|this|that)\s+", "", clause_prefix, flags=re.IGNORECASE)
    # Only a remaining noun-like prefix is a bound permission qualifier
    # (``Database permission``); discourse and request prefixes are not.
    if clause_prefix and re.fullmatch(
        r"[A-Za-z][A-Za-z0-9_./-]*(?:\s+[A-Za-z0-9_./-]+){0,3}", clause_prefix
    ):
        return False
    return bool(re.fullmatch(
        r"(?:that\s+)?(?:permission|authorization|authority)\s+"
        r"(?:(?:is|was|has\s+been|have\s+been)\s+)?(?:revoked|withdrawn)",
        text,
        re.IGNORECASE,
    ))


PR_LIFECYCLE_RE = re.compile(
    r"\b(?P<open>create|open|file|draft|submit|raise)\b.{0,40}?"
    r"\b(?:draft\s+|ready\s+)?(?:pull\s+request|PR)\b|"
    r"\b(?P<mutation>edit|update|rename|ready|convert|reopen|label)\b.{0,40}?"
    r"\b(?:pull\s+request|PR)\b|"
    r"\b(?P<mutation_tail>pull\s+request|PR)\b.{0,24}"
    r"\b(?:edit|update|rename|ready|convert|reopen|label)\b|"
    r"\b(?P<cancel>cancel)\s+(?:(?:this|that|the(?:\s+existing)?|an?|existing)\s+)?"
    r"(?:pull\s+request|PR)\b|"
    r"\b(?P<close>close)\b.{0,24}\b(?:pull\s+request|PR)\b|"
    r"\b(?P<implicit_cancel>cancel\s+(?:it|that\s+(?:request|PR))|scratch\s+that)\b|"
    r"(?P<cjk_open>(?:再次)?(?:创建|提(?:个)?|发起|开启|打开)\s*(?:草稿\s*)?(?:PR|拉取请求))|"
    r"(?P<cjk_cancel>(?:取消|撤销)\s*(?:它|该请求|PR|拉取请求))|"
    r"(?P<cjk_close>关闭\s*(?:PR|拉取请求))",
    re.IGNORECASE,
)


def delivery_occurrences(clause: str) -> list[re.Match[str]]:
    """Return action verbs, excluding Git-operation objects such as ``abort rebase``."""
    occurrences: list[re.Match[str]] = []
    for match in DELIVERY_ACTION_RE.finditer(clause):
        action = canonical_action(match)
        prefix = clause[max(0, match.start() - 40) : match.start()]
        if action == "commit":
            object_prefix = re.split(
                r",|\b(?:then|but|while)\b|[:：]|\s[-–—]\s",
                clause[: match.start()],
                flags=re.IGNORECASE,
            )[-1]
            if re.search(r"\bcherry[ -]pick(?:\s+[\w-]+){0,5}\s+$", object_prefix, re.IGNORECASE):
                continue
        if action in {"rebase", "merge", "cherry-pick"} and re.search(
            r"\b(?:abort|continue)(?:\s+[\w-]+){0,3}\s+$", prefix, re.IGNORECASE
        ):
            continue
        if action == "branch" and not re.search(
            r"(?:^|\b(?:run|execute)\s+)git(?:\s+(?:-C|-c|--git-dir|--work-tree)(?:=\S+|\s+\S+))*\s+$",
            prefix,
            re.IGNORECASE,
        ):
            continue
        occurrences.append(match)
    return occurrences


def postfix_denied_actions(actions: list[re.Match[str]], clause: str) -> set[int]:
    """Return actions denied by a postfix prohibition in one English clause.

    A singular predicate binds to its nearest preceding action (``push is
    forbidden``), while a plural predicate binds to the preceding coordinated
    action list (``commit and push are not allowed``).
    """
    denied: set[int] = set()
    for match in POSTFIX_DENIAL_RE.finditer(clause):
        before_status = clause[: match.start()]
        boundary = max(
            before_status.rfind(","),
            *(
                occurrence.start()
                for occurrence in re.finditer(r"\b(?:while|whereas)\b", before_status, re.IGNORECASE)
            ),
            -1,
        )
        preceding = [
            index for index, action in enumerate(actions)
            if action.end() <= match.start() and action.start() > boundary
        ]
        if not preceding:
            continue
        if (match.group("verb") or "").lower() == "are":
            denied.update(preceding)
        else:
            denied.add(preceding[-1])
    return denied


def is_leading_negative_action_list(prefix: str) -> bool:
    """Whether a comma-separated prefix is only a denied delivery-action list."""
    match = re.match(
        r"\s*(?:(?:you\s+)?(?:do\s+not|don't|never|must\s+not|may\s+not|"
        r"cannot|can't)|no)\s+(?P<actions>.+)",
        prefix,
        re.IGNORECASE,
    )
    if not match:
        return False
    action_list = re.sub(r"(?:,|\band\b|\bor\b)\s*$", "", match.group("actions"), flags=re.IGNORECASE)
    action_list = action_list.strip()
    if not action_list:
        return False
    return all(
        DELIVERY_ACTION_RE.fullmatch(item.strip())
        for item in re.split(r"\s*(?:,|\band\b|\bor\b)\s*", action_list, flags=re.IGNORECASE)
    )


def imperative_actions(
    action: re.Match[str], segment_prefix: str, suffix: str
) -> set[str]:
    """Return a coordinated imperative chain only when it ends in command syntax."""
    action_form = " ".join(action.group(0).lower().split())
    if action_form not in BASE_DELIVERY_ACTIONS and action_form != "clean up":
        return set()
    if not re.fullmatch(
        r"\s*(?:(?:please|kindly)\s+|go\s+ahead\s+and\s+|then\s+)?",
        segment_prefix,
        re.IGNORECASE,
    ):
        return set()
    actions = {canonical_action(action)}
    remainder = suffix.strip().lower()
    if remainder == ",":
        return actions
    while coordinate := re.match(
        r"(?:,\s*(?:(?:and|then)\s+)?|\b(?:and|or|then)\s+)"
        r"(?P<action>stage|commit|push|merge|rebase|tag|release|publish|cleanup|clean\s+up|"
        r"delete|sync|integrate|deliver|squash|resolve|continue|checkpoint|normalize|pull|fetch|"
        r"fast-forward|fast forward|cherry-pick|cherry pick|abort)\b\s*",
        remainder,
    ):
        actions.add(ACTION_CANONICAL[" ".join(coordinate.group("action").lower().split())])
        remainder = remainder[coordinate.end() :]
    if re.search(
        r"\b(?:explain|describe|check|confirm|verify)\b.{0,40}\b(?:how\s+to|whether|if)\b"
        r".{0,40}" + DELIVERY_ACTION_RE.pattern,
        remainder,
        re.IGNORECASE,
    ):
        return set()
    if not remainder or re.match(
        r"(?:locally|now|immediately|directly|all|only|every|each)\b|"
        r"(?:it|them|this|that|these|those|the|a|an|my|our|your|their)\b|"
        r"to\s+origin\b|"
        r"(?:from\s+)?(?:origin|remote|upstream|refs?)\b|"
        r"onto\s+main\b|"
        r"after\s+(?:the\s+)?tests?\b|"
        r"(?:fix(?:es)?|changes?)\s+(?:for|to)\s+(?:the\s+)?(?:existing|open)\s+pr\s+branch\b|"
        r"(?:version|artifact|tag)\b",
        remainder,
    ):
        return actions
    return set()


def affirmative_action(clause: str, action: re.Match[str], segment_prefix: str, suffix: str) -> set[str]:
    """Return one explicitly authorized action, or an imperative action chain."""
    imperative = imperative_actions(action, segment_prefix, suffix)
    if imperative:
        return imperative
    if canonical_action(action) == "commit" and re.search(
        r"\bcreate\b.{0,80}\b(?:local\s+)?commit\b", clause[: action.end()], re.IGNORECASE
    ):
        return {"commit"}
    if re.match(
        r"\s*(?:please\s+)?(?:implement|fix|update|change|refactor|build|create|add|remove)\b"
        r".{0,160}\band\s*$",
        segment_prefix,
        re.IGNORECASE,
    ) and re.match(
        r"\s*(?:it|them|this|that|these|those|the|a|an|my|our|your|their|to\s+origin)\b",
        suffix,
        re.IGNORECASE,
    ):
        # A source-change command may coordinate a separately owned Git action.
        # This only classifies the delivery clause; search() still returns a
        # handoff plan and never transfers execution authorization to the source owner.
        return {canonical_action(action)}
    action_pattern = re.escape(action.group(0))
    if re.search(
        r"\b(?:can|could|would|will)\s+you(?:\s+please)?\s+" + action_pattern + r"\b|"
        r"\b(?:i\s+)?(?:authorize(?:d)?|permit(?:ted)?)\s+(?:you\s+)?to\s+" + action_pattern + r"\b|"
        r"\bi\s+give\s+you\s+permission\s+to\s+" + action_pattern + r"\b|"
        r"\b(?:permission\s+(?:is\s+)?granted|authorized|permitted|allowed)\s+(?:to\s+)?"
        + action_pattern + r"\b|"
        r"\bmay\s+be\s+" + action_pattern + r"\b|"
        r"\byou\s+may\s+" + action_pattern + r"\b|"
        r"\byou\s+have\s+permission\s+to\s+" + action_pattern + r"\b",
        clause,
        re.IGNORECASE,
    ):
        return {canonical_action(action)}
    if re.search(r"ing(?:\s+up)?$", action.group(0).lower()) and re.search(
        r"\b(?:is|are|was|were|has\s+been|have\s+been)\s+"
        r"(?:explicitly\s+)?(?:authorized|permitted)\b",
        suffix,
        re.IGNORECASE,
    ):
        return {canonical_action(action)}
    if re.search(r"\b(?:ready|approved)\s+for\s*$", clause[: action.start()], re.IGNORECASE):
        return {canonical_action(action)}
    return set()


def is_authorization_status_question(clause: str) -> bool:
    """Keep a question about permission distinct from a permission grant."""
    indirect = re.match(
        r"\s*(?:check|confirm|determine|verify|tell\s+me|help\s+me\s+(?:check|confirm))\s+"
        r"(?:whether|if)\b",
        clause,
        re.IGNORECASE,
    )
    if indirect:
        return True
    inverted = r"\s*(?:are\s+you\s+(?:explicitly\s+)?(?:authorized|permitted|allowed)\s+to|do\s+you\s+have\s+permission\s+to|is\s+permission(?:\s+to\s+[\w-]+(?:\s+[\w-]+)*)?\s+granted(?:\s+to)?|is\s+(?:the\s+)?(?:reviewed\s+)?branch\s+ready\s+for|is\s+(?:this\s+|the\s+)?branch\s+approved\s+for)\b"
    if re.match(inverted, clause, re.IGNORECASE):
        return True
    if "?" not in clause:
        return False
    if re.match(r"\s*(?:how|what|when|which)\b", clause, re.IGNORECASE):
        return True
    return bool(
        re.match(
            inverted,
            clause,
            re.IGNORECASE,
        )
    ) or bool(re.search(
        r"\b(?:ready|approved|authorized|allowed|permitted|permission)\b",
        clause,
        re.IGNORECASE,
    ))


def english_delivery_actions(query: str) -> tuple[set[str], set[str]]:
    """Parse affirmative and revoked Git delivery actions from English clauses."""
    decisions: dict[str, bool] = {}
    for clause in re.split(r"(?<=[.;!?])|\bbut\b", query, flags=re.IGNORECASE):
        if is_authorization_status_question(clause):
            continue
        actions = delivery_occurrences(clause)
        if REVOCATION_RE.search(clause) and not re.search(r"\b(?:pull\s+request|PR)\b", clause, re.IGNORECASE):
            if not actions:
                decisions = {action: False for action in decisions}
            else:
                for action in actions:
                    decisions[canonical_action(action)] = False
            continue
        postfix_denied = postfix_denied_actions(actions, clause)
        for index, action in enumerate(actions):
            prefix = clause[: action.start()]
            segment_start = clause.rfind(",", 0, action.start()) + 1
            segment_prefix = clause[segment_start : action.start()]
            suffix = clause[action.end() :]
            action_name = canonical_action(action)
            if (
                PREFIX_DENIAL_RE.search(segment_prefix)
                or is_leading_negative_action_list(prefix)
                or index in postfix_denied
            ):
                decisions[action_name] = False
                continue
            for authorized_action in affirmative_action(clause, action, segment_prefix, suffix):
                decisions[authorized_action] = True
    return (
        {action for action, decision in decisions.items() if decision},
        {action for action, decision in decisions.items() if not decision},
    )


def action_has_git_context(action: str, query: str) -> bool:
    """Require a Git-shaped object or destination for each English action."""
    non_git_homonyms = {
        "delete": r"\bbranch\s+(?:node|condition|case)\b",
        "sync": r"\bbranch\s+office\b|\bremote\s+(?:headquarters|office)\b",
        "integrate": r"\b(?:bank|retail)\s+branch\b|\bmain\s+(?:reporting|processing)\s+system\b",
        "checkpoint": r"\b(?:machine-learning|data-processing|model|training)\s+(?:work|task)\b",
        "normalize": r"\b(?:patient|medical|browser)\s+history\b",
    }
    patterns = {
        "stage": r"\bstag(?:e|ed|ing)\b(?:\s+\w+){0,3}\s+(?:changes?|scope|files)\b",
        "commit": r"\bcommit(?:ted|ting)?\b(?:\s+[\w-]+){0,7}\s+(?:locally|changes?|slice|fixup|milestone)\b|"
        r"\bcommit(?:ted|ting)?\b(?:\s+\w+){0,5}\s+branch\b(?!\s+selection\b)|"
        r"\bcreate\b.{0,80}\b(?:local\s+)?commit\b|\bcommit\b\s+after\s+(?:the\s+)?tests?\b",
        "push": r"\bpush(?:ed|ing)?\b(?:\s+\w+){0,6}\s+(?:changes?|commits)\b|"
        r"\bpush(?:ed|ing)?\b(?:\s+\w+){0,6}\s+branch\b(?!\s+button\b)|\bpush\b\s+to\s+(?:origin|remote)\b|"
        r"\bbranch\b(?:\s+\w+){0,4}\s+\bpushed\b",
        "merge": r"\bmerg(?:e|ed|ing)\b(?:\s+\w+){0,3}\s+branch\b|"
        r"\bbranch\b(?:\s+\w+){0,4}\s+\bmerging\b",
        "rebase": r"\brebas(?:e|ed|ing)\b(?:\s+\w+){0,3}\s+(?:branch|onto\s+main)\b",
        "tag": r"\btag(?:ged|ging)?\b(?:\s+\w+){0,3}\s+(?:version|package|artifact)\b",
        "release": r"\breleas(?:e|ed|ing)\b(?:\s+\w+){0,3}\s+(?:version|package|artifact|tag)\b",
        "publish": r"\bpublish(?:ed|ing)?\b(?:\s+\w+){0,3}\s+(?:package|artifact|release)\b",
        "cleanup": r"\bclean(?:\s+up|ing\s+up)?\b(?:\s+\w+){0,4}\s+(?:working\s+tree|repo(?:sitory)?|git)\b",
        "delete": r"\bdelete\b(?:\s+\w+){0,3}\s+(?:temporary\s+)?branch\b",
        "sync": r"\bsync\b(?:\s+[\w-]+){0,4}\s+branch\b(?:\s+[\w-]+){0,3}\s+to\s+"
        r"(?:remote|origin|upstream)\b(?!\s+[\w-])",
        "integrate": r"\bintegrate\b(?:\s+\w+){0,3}\s+branch\b(?:\s+\w+){0,3}\s+into\s+main\b",
        "deliver": r"\bdeliver\b(?:\s+[\w-]+){0,8}\s+(?:reviewed\s+)?(?:changes?|branch|scope)\b",
        "squash": r"\bsquash\b(?:\s+\w+){0,6}\s+branch\b(?:\s+\w+){0,3}\s+into\s+main\b",
        "resolve": r"\bresolve\b(?:\s+\w+){0,5}\s+(?:conflicts?|hunks?)\b|\bconflicts?\b.{0,80}\bresolve\b",
        "continue": r"\bcontinue\b(?:\s+\w+){0,3}\s+(?:rebase|merge)\b",
        "checkpoint": r"\bcheckpoint\b(?:\s+[\w-]+){0,8}\s+(?:paths?|changes?)\b",
        "normalize": r"\bnormalize\b(?:\s+\w+){0,8}\s+(?:fixups?|checkpoint|task\s+tree)\b|"
        r"\bnormalize\b(?:\s+\w+){0,6}\s+(?:git|commit|branch)\s+history\b",
        "pull": r"\bpull\b(?:\s+\w+){0,5}\s+(?:from\s+)?(?:origin|remote|upstream)\b|"
        r"\bpull\b(?:\s+\w+){0,4}\s+branch\b",
        "fetch": r"\bfetch\b(?:\s+(?:--[\w-]+|\w+)){0,5}\s+(?:origin|upstream)\b|"
        r"\bfetch\s+(?:the\s+)?remote\s+(?:refs?|branch(?:es)?)\b|"
        r"\bfetch\b(?:\s+(?:--[\w-]+|\w+)){0,5}\s+refs?\b",
        "fast-forward": r"\bfast[ -]forward\b(?:\s+\w+){0,5}\s+(?:branch|onto\s+main)\b|"
        r"\bbranch\b(?:\s+\w+){0,5}\s+fast-forward(?:ed|ing)?\b",
        "cherry-pick": r"\bcherry[ -]pick\b(?:\s+\w+){0,5}\s+(?:commit|sha|branch)\b",
        "abort": r"\babort\b(?:\s+\w+){0,4}\s+(?:rebase|merge|cherry-pick)\b",
    }
    for clause in re.split(r"[.;!?]", query):
        all_occurrences = delivery_occurrences(clause)
        occurrences = [match for match in all_occurrences if canonical_action(match) == action]
        if not occurrences:
            continue
        for occurrence in occurrences:
            # Context must bind to this occurrence, not another same-named verb
            # elsewhere in the sentence (for example, a database commit followed
            # by a separate Git commit).
            occurrence_index = all_occurrences.index(occurrence)
            local_start = all_occurrences[occurrence_index - 1].end() if occurrence_index else 0
            local_end = (
                all_occurrences[occurrence_index + 1].start()
                if occurrence_index + 1 < len(all_occurrences)
                else len(clause)
            )
            local = clause[local_start:local_end]
            occurrence_tail = local[occurrence.start() - local_start :]
            if action == "push" and re.search(
                r"\bpush\b(?:\s+\w+){0,3}\s+button\b", occurrence_tail, re.IGNORECASE
            ):
                continue
            if action == "commit" and re.search(
                r"\bcommit\b(?:\s+\w+){0,8}\s+(?:to|into)\s+(?:the\s+)?"
                r"(?:local\s+)?(?:database|db|transaction)\b|"
                r"\bcommit\b.{0,80}\bbranch\s+selection\b",
                occurrence_tail,
                re.IGNORECASE,
            ):
                continue
            if action in non_git_homonyms and re.search(
                non_git_homonyms[action], occurrence_tail, re.IGNORECASE
            ):
                continue
            if re.search(patterns[action], local, re.IGNORECASE):
                return True
    return False


def requests_pull_request(query: str) -> bool:
    """Return whether the final instruction still affirmatively asks to create a PR."""
    requested = False
    for clause in re.split(r"(?<=[.;!?])|\bbut\b", query, flags=re.IGNORECASE):
        match = re.search(
            r"(?:^|[,;]|\b(?:and|then)\b)\s*(?:please\s+)?"
            r"(?:open|create|publish|submit|raise|file|draft)\b.{0,40}\b(?:draft\s+|ready\s+)?"
            r"(?:pull\s+request|PR)\b",
            clause,
            re.IGNORECASE,
        )
        chinese_pr = bool(re.search(r"(?:创建|提交|发起|开启|打开|提(?:个)?|建)\s*(?:草稿\s*)?(?:PR|pr|拉取请求)", clause))
        denied = bool(re.search(
            r"(?:do\s+not|don't|never|must\s+not|under\s+no\s+circumstances)\s+"
            r"(?:\w+\s+){0,4}(?:pull\s+request|PR)\b|"
            r"(?:cancel|revoke|取消|撤销|不要|禁止|不得|不允许).{0,16}"
            r"(?:pull\s+request|PR|pr|拉取请求)|"
            r"(?:pull\s+request|PR)\b.{0,20}(?:revoked|withdrawn|cancelled|canceled)",
            clause,
            re.IGNORECASE,
        ))
        if denied:
            requested = False
        elif match or chinese_pr:
            requested = True
        elif requested and REVOCATION_RE.search(clause):
            requested = False
    return requested


CHINESE_ACTION_CANONICAL = {
    "暂存": "stage", "提交": "commit", "推送": "push", "合并": "merge",
    "变基": "rebase", "打标签": "tag", "发布": "release", "清理": "cleanup",
    "拉取": "pull",
}
CHINESE_STATUS_QUESTION_RE = re.compile(r"^\s*(?:(?:如何|怎么|怎样|是否|能否|可否|什么时候|哪个)|(?:帮我)?(?:确认|检查|查看).{0,12}(?:是否|能否|可否)).*(?:暂存|提交|推送|合并|变基|打标签|发布|清理)")
CHINESE_APPROVAL_PENDING_RE = re.compile(r"(?:暂存|提交|推送|合并|变基|打标签|发布|清理).{0,12}(?:需要|等待|尚未|待定|待)批准|(?:需要|等待|尚未|待定|待)批准.{0,12}(?:暂存|提交|推送|合并|变基|打标签|发布|清理)")


def chinese_delivery_actions(query: str) -> tuple[set[str], set[str]]:
    """Parse explicit Chinese Git commands and their later revocations."""
    decisions: dict[str, bool] = {}
    for clause in re.split(r"[，。；;.!?]|但|随后", query):
        if CHINESE_STATUS_QUESTION_RE.search(clause):
            continue
        actions = {
            canonical for term, canonical in CHINESE_ACTION_CANONICAL.items() if term in clause
        }
        if not actions:
            if "取消授权" in clause or "撤销授权" in clause:
                decisions = {action: False for action in decisions}
            continue
        if (
            any(negation in clause for negation in CHINESE_NEGATION)
            or "不能" in clause
            or "取消授权" in clause
            or CHINESE_APPROVAL_PENDING_RE.search(clause)
        ):
            for action in actions:
                decisions[action] = False
        elif re.match(r"\s*(?:请|麻烦|请你|你可以)", clause) or re.search(r"(?:更改|改动|分支|仓库|工作区|本地|main)", clause):
            for action in actions:
                decisions[action] = True
    return (
        {action for action, decision in decisions.items() if decision},
        {action for action, decision in decisions.items() if not decision},
    )


def chinese_action_has_git_context(action: str, query: str) -> bool:
    if action == "stage":
        return "暂存" in query
    if action == "pull":
        return bool(re.search(r"拉取.{0,12}(?:远程|origin|上游|分支|仓库|Git)", query, re.IGNORECASE))
    return bool(re.search(r"更改|改动|分支|仓库|工作区|本地|测试|构建|Git|main", query))


def chinese_occurrence_has_git_context(action: str, clause: str) -> bool:
    """Keep each CJK action bound to its own object and negation clause."""
    if re.search(r"(?:数据库|db|事务|按钮)", clause, re.IGNORECASE):
        return False
    return chinese_action_has_git_context(action, clause)


class IntentEvent(NamedTuple):
    """One delivery-shaped occurrence, retaining the evidence needed by routing."""

    span: tuple[int, int]
    segment: str
    action: str
    context: bool
    modality: str
    owner: str


class DeliveryIntent(NamedTuple):
    events: tuple[IntentEvent, ...]
    global_barrier: bool
    pull_request_requested: bool
    authorized: bool


def occurrence_window(segment: str, occurrence: re.Match[str]) -> tuple[str, str]:
    """Return the grammatical neighbourhood of one action occurrence.

    A segment may contain more than one spelling of the same action.  Do not
    let a prohibition, imperative, or object from one occurrence decide the
    other: ``do not commit Git changes, then commit this database value`` has
    two independent commits.
    """
    before = segment[: occurrence.start()]
    after = segment[occurrence.end() :]
    # ``and`` remains part of one coordinated imperative chain (``commit and
    # push this branch``); ``then`` and commas form separate occurrences.
    starts = [match.end() for match in re.finditer(r",\s*|\b(?:then|but|while)\b\s*", before, re.IGNORECASE)]
    ends = [match.start() for match in re.finditer(r",|\b(?:then|but|while)\b", after, re.IGNORECASE)]
    return before[max(starts, default=0) :], after[: min(ends, default=len(after))]


def explicit_action_authorization(action: re.Match[str], segment: str) -> bool:
    """Whether this occurrence is an explicit grant, rather than a bare command."""
    action_pattern = re.escape(action.group(0))
    prefix, suffix = occurrence_window(segment, action)
    scope = prefix + action.group(0) + suffix
    return bool(re.search(
        r"\b(?:i\s+)?(?:authorize(?:d)?|permit(?:ted)?)\s+(?:you\s+)?to\s+" + action_pattern + r"\b|"
        r"\bi\s+give\s+you\s+permission\s+to\s+" + action_pattern + r"\b|"
        r"\b(?:permission\s+(?:is\s+)?granted|authorized|permitted|allowed)\s+(?:to\s+)?"
        + action_pattern + r"\b|\b(?:the\s+)?branch\s+may\s+be\s+" + action_pattern + r"\b|"
        r"\bpermission\s+to\s+" + action_pattern + r"\b.{0,80}\b(?:is\s+)?granted\b|"
        r"\bpushing\b.{0,40}\b(?:is\s+)?authorized\b|"
        r"\byou\s+(?:may|have\s+permission\s+to)\s+" + action_pattern + r"\b",
        scope,
        re.IGNORECASE,
    ))


def cli_action_at_occurrence(action: str, segment: str, occurrence: re.Match[str]) -> bool:
    """Recognize a concrete Git CLI invocation, including option-bearing forms."""
    head = segment[: occurrence.start()]
    tail = segment[occurrence.end() :]
    cli_value = r'(?:"[^"]+"|\'[^\']+\'|\S+)'
    global_options = (
        r"(?:\s+(?:-C|-c|--git-dir|--work-tree)(?:=" + cli_value + r"|\s+" + cli_value + r"))*"
    )
    if not re.search(
        r"(?:^\s*|\b(?:run|execute|then|but|while|therefore)\s+|(?:然后|随后)\s+|[,:：]\s*|\s[-–—]\s*)git"
        + global_options + r"\s+$",
        head,
        re.IGNORECASE,
    ):
        return False
    if action == "abort":
        return bool(re.search(r"^\s*$", head) or re.search(r"\bgit\s+(?:rebase|merge|cherry-pick)\s+--$", head, re.IGNORECASE))
    if action == "rebase" and re.match(r"\s+--abort\b", tail, re.IGNORECASE):
        return True
    return True


def occurrence_has_git_context(action: str, segment: str, occurrence: re.Match[str]) -> bool:
    """Require Git-shaped evidence that belongs to this action occurrence."""
    if cli_action_at_occurrence(action, segment, occurrence):
        return True
    if action in {"switch", "checkout", "reset", "revert", "restore", "branch", "add", "rm", "clean"}:
        # These extra destructive forms are intentionally discoverable only as
        # bounded concrete Git CLI invocations, never as prose homonyms.
        return False
    if action == "abort" and re.search(
        r"\bgit\s+(?:rebase|merge|cherry-pick)\s+--\s*$", segment[: occurrence.start()], re.IGNORECASE
    ):
        return True
    prefix, suffix = occurrence_window(segment, occurrence)
    if re.search(r"\b(?:discuss|explain|describe|how\s+to|whether)\b", prefix, re.IGNORECASE):
        return False
    local = prefix + occurrence.group(0) + suffix
    if action == "commit" and re.search(r"\b(?:database|db|transaction)\b", local, re.IGNORECASE):
        return False
    if action == "abort" and re.search(r"\babort\b.{0,16}\bmerge\s+request\b", local, re.IGNORECASE):
        return False
    if action == "release" and re.search(r"\brelease\s+(?:the\s+)?(?:package(?:[ -])lock(?:file|\.json)?|dependency\s+lock|resource\s+lock)\b", local, re.IGNORECASE):
        return False
    if action == "release" and re.search(r"\brelease\s+tag\b", local, re.IGNORECASE):
        return True
    return action_has_git_context(action, local)


def occurrence_modality(
    action: re.Match[str], segment: str, inquiry: bool
) -> str:
    """Classify exactly one delivery occurrence; never reuse action-level sets."""
    if inquiry:
        return "inquiry"
    prefix, suffix = occurrence_window(segment, action)
    postfix = POSTFIX_DENIAL_RE.search(suffix)
    postfix_is_local = postfix is not None and not re.search(
        r"[:：]|\s[-–—]\s", suffix[: postfix.start()]
    )
    if (
        PREFIX_DENIAL_RE.search(prefix)
        or is_leading_negative_action_list(prefix)
        or (postfix_is_local and not delivery_occurrences(suffix[: postfix.start()]))
        or "without authorization" in prefix.lower()
    ):
        return "deny"
    if cli_action_at_occurrence(canonical_action(action), segment, action):
        return "command"
    if explicit_action_authorization(action, segment):
        return "reauthorize"
    if canonical_action(action) in affirmative_action(segment, action, prefix, suffix):
        return "command"
    return "mention"


def occurrence_is_inquiry(action: re.Match[str], segment: str) -> bool:
    prefix, suffix = occurrence_window(segment, action)
    action_pattern = re.escape(action.group(0))
    return bool(re.search(
        r"\b(?:can|may)\s+i\s*$|\bdo\s+you\s+have\s+permission\s+to\s*$|"
        r"\bare\s+you\s+(?:authorized|permitted|allowed)\s+to\s*$|"
        r"\bis\s+permission\s+granted\s+to\s*$",
        prefix,
        re.IGNORECASE,
    )) or bool(re.search(
        r"\bis\s+permission\s+to\s+" + action_pattern
        + r"\b(?:\s+[\w-]+){0,6}\s+granted\b",
        prefix + action.group(0) + suffix,
        re.IGNORECASE,
    ))


def occurrence_is_in_leading_denial(segment: str, occurrence: re.Match[str]) -> bool:
    """Bind ``do not stage, commit, or push`` to that one coordinated list."""
    first = next(iter(delivery_occurrences(segment)), None)
    if first is None or occurrence.start() < first.start():
        return False
    leading = segment[: first.start()]
    if not PREFIX_DENIAL_RE.search(leading):
        return False
    if re.search(r"\b(?:then|but|while)\b|[,;:：]|\s[-–—]\s", leading, re.IGNORECASE):
        return False
    between = segment[first.end() : occurrence.start()]
    return not bool(re.search(r"\b(?:then|but|while)\b", between, re.IGNORECASE))


def parse_delivery_intent(query: str) -> DeliveryIntent:
    """Parse ordered delivery occurrences without allowing one occurrence to borrow another's context.

    The existing action reducers remain the compatibility layer for the mature
    English/CJK grammar, while this structure is the single routing input.
    """
    barrier_pattern = re.compile(
        GLOBAL_DELIVERY_FORBIDDEN_RE.pattern + r"|Git\s+state\s+must\s+not\s+change|"
        r"(?:禁止|不得|不允许).{0,12}(?:修改|更改|变更).{0,12}Git\s*(?:状态|state)?",
        re.IGNORECASE,
    )
    barrier = bool(barrier_pattern.search(query) or re.search(
        r"Git\s*(?:mutation|操作).{0,16}(?:禁止|不得|不允许)|"
        r"(?:禁止|不得|不允许).{0,12}(?:修改|更改|变更).{0,12}Git\s*(?:状态|state)?",
        query,
        re.IGNORECASE,
    ))
    revocation_pattern = re.compile(
        REVOCATION_RE.pattern + r"|\b(?:withdraw|rescind|cancel)\s+(?:that\s+)?(?:permission|authorization)\b|"
        r"\b(?:permission|authorization)(?:\s+to\s+(?:[a-z]+(?:[ -][a-z]+){0,2}))?\s+"
        r"(?:(?:is|was|has\s+been|have\s+been)\s+)?(?:revoked|withdrawn)\b|"
        r"\b[a-z]+(?:[ -][a-z]+){0,2}\s+(?:permission|authorization)\s+"
        r"(?:(?:is|was|has\s+been|have\s+been)\s+)?(?:revoked|withdrawn)\b|"
        r"授权已撤回|我撤回授权|取消授权|撤销授权",
        re.IGNORECASE,
    )
    events: list[IntentEvent] = []
    pending_pr_lifecycle = 0
    prior_pr_lifecycle = False
    # A full stop only terminates a sentence when followed by whitespace or
    # end-of-input, so ``git -c protocol.version=2 fetch origin`` stays one
    # concrete CLI event rather than being split at the config key's dot.
    for segment_match in re.finditer(
        r"(?:(?!\.(?=\s|$))[^;!?。；])+(?:[;!?。；]|\.(?=\s|$))?",
        query,
    ):
        segment = segment_match.group(0)
        inquiry = (
            is_authorization_status_question(segment)
            or bool(CHINESE_STATUS_QUESTION_RE.search(segment))
            or bool(re.search(r"\b(?:please\s+)?(?:confirm|check|want|wonder)\s+whether\b", segment, re.IGNORECASE))
            or "想知道能否" in segment
            or bool(re.search(r"我想知道是否可以", segment))
        )
        coordinated_inquiry = bool(re.match(r"\s*(?:can|may)\s+i\b", segment, re.IGNORECASE) and "?" in segment)
        for barrier_match in barrier_pattern.finditer(segment):
            events.append(IntentEvent(
                (segment_match.start() + barrier_match.start(), segment_match.start() + barrier_match.end()),
                segment, "barrier", False, "barrier", "delivery"
            ))
        for revoke_match in revocation_pattern.finditer(segment):
            target = targeted_revocation_action(segment[max(0, revoke_match.start() - 48) : revoke_match.end()])
            if target is None and not is_bare_revocation(revoke_match, segment):
                continue
            events.append(IntentEvent(
                (segment_match.start() + revoke_match.start(), segment_match.start() + revoke_match.end()),
                segment, "revoke:" + target if target else "revoke", False, "revoke", "delivery"
            ))
        segment_pr_lifecycle_seen = False
        last_pr_end = 0
        for pr_match in PR_LIFECYCLE_RE.finditer(segment):
            if (
                re.search(r"\bfor\s+the\s+$", segment[:pr_match.start()], re.IGNORECASE)
                or re.search(r"\bPR\s+branch\b", segment, re.IGNORECASE)
            ):
                continue
            kind = pr_match.lastgroup
            if kind in {"open", "cjk_open"}:
                local_prefix = segment[max(last_pr_end, segment.rfind(",", 0, pr_match.start()) + 1) : pr_match.start()]
                pr_denied = bool(re.search(
                    r"(?:do\s+not|don't|must\s+not|under\s+no\s+circumstances|不要|禁止|不得)",
                    local_prefix,
                    re.IGNORECASE,
                ))
                pr_action = "pr-denied" if pr_denied else "pr-open"
                if pr_action == "pr-open":
                    pending_pr_lifecycle += 1
                    segment_pr_lifecycle_seen = True
                elif pr_action == "pr-denied":
                    # A denied additional open preserves an earlier pending PR
                    # as the immediately preceding lifecycle antecedent.
                    segment_pr_lifecycle_seen = True
            elif kind in {"implicit_cancel", "cjk_cancel", "cancel"} and pending_pr_lifecycle and (
                segment_pr_lifecycle_seen or prior_pr_lifecycle
            ) and not re.search(r"\bexisting\b|已有", pr_match.group(0), re.IGNORECASE) and not re.sub(
                r"(?:\s|,|，|;|；|\bthen\b|\bbut\b|\bwhile\b|随后|然后)+", "",
                segment[last_pr_end : pr_match.start()], flags=re.IGNORECASE,
            ):
                pr_action = "pr-cancel-pending"
                pending_pr_lifecycle -= 1
                segment_pr_lifecycle_seen = True
            elif kind == "close":
                pr_action = "pr-close"
            elif kind in {"mutation", "mutation_tail"}:
                pr_action = "pr-mutation"
            else:
                # Cancelling a named existing PR is a publishing mutation, not
                # cancellation of a pending creation request.
                pr_action = "pr-cancel-mutation"
            events.append(IntentEvent(
                (segment_match.start() + pr_match.start(), segment_match.start() + pr_match.end()),
                segment, pr_action, True, "command", "publishing"
            ))
            last_pr_end = pr_match.end()
        prior_pr_lifecycle = segment_pr_lifecycle_seen and pending_pr_lifecycle > 0
        occurrences = delivery_occurrences(segment)
        coordinated_commands: list[tuple[int, int, set[str]]] = []
        for occurrence in occurrences:
            prefix, _ = occurrence_window(segment, occurrence)
            suffix_end = min([
                match.start() for match in re.finditer(r"\b(?:then|but|while)\b", segment[occurrence.end() :], re.IGNORECASE)
            ] or [len(segment) - occurrence.end()])
            suffix = segment[occurrence.end() : occurrence.end() + suffix_end]
            actions = imperative_actions(occurrence, prefix, suffix)
            if actions:
                coordinated_commands.append((occurrence.start(), occurrence.end() + suffix_end, actions))
        for occurrence in occurrences:
            action = canonical_action(occurrence)
            modality = occurrence_modality(
                occurrence,
                segment,
                (coordinated_inquiry or (inquiry and not re.search(r"\b(?:then|but|while)\b|[,;:：]|\s[-–—]\s|随后|然后", segment, re.IGNORECASE)))
                or occurrence_is_inquiry(occurrence, segment),
            )
            if occurrence_is_in_leading_denial(segment, occurrence):
                modality = "deny"
            if modality == "mention" and any(
                action in actions
                and start <= occurrence.start() < end
                for start, end, actions in coordinated_commands
            ):
                modality = "command"
            occurrence_context = occurrence_has_git_context(action, segment, occurrence)
            if modality == "deny" and not re.search(
                r"\b(?:database|db|transaction|button)\b",
                occurrence_window(segment, occurrence)[0] + occurrence.group(0) + occurrence_window(segment, occurrence)[1],
                re.IGNORECASE,
            ):
                occurrence_context = True
            events.append(IntentEvent(
                span=(segment_match.start() + occurrence.start(), segment_match.start() + occurrence.end()),
                segment=segment,
                action=action,
                context=occurrence_context or any(
                    action in actions
                    and start <= occurrence.start() < end
                    and any(
                        start <= peer.start() < end
                        and occurrence_has_git_context(canonical_action(peer), segment, peer)
                        for peer in occurrences
                    )
                    for start, end, actions in coordinated_commands
                ),
                modality=modality,
                owner="delivery",
            ))
        for term, action in CHINESE_ACTION_CANONICAL.items():
            for cjk_match in re.finditer(re.escape(term), segment):
                prior = list(re.finditer(r"[，；]|但|随后|然后", segment[: cjk_match.start()]))
                following = re.search(r"[，；]|但|随后|然后", segment[cjk_match.end() :])
                local_start = prior[-1].end() if prior else 0
                local_end = cjk_match.end() + following.start() if following else len(segment)
                local = segment[local_start:local_end]
                denied = any(negation in local for negation in CHINESE_NEGATION) or "不能" in local
                explicit = bool(re.search(r"(?:你可以|允许你|授权你|已授权).{0,12}" + re.escape(term), local))
                command = bool(re.match(r"\s*(?:请|麻烦|请你)", local)) or bool(
                    re.search(r"(?:更改|改动|分支|仓库|工作区|本地|测试|构建|Git|main)", local)
                ) or explicit
                local_inquiry = bool(CHINESE_STATUS_QUESTION_RE.search(local)) or "想知道能否" in local or "我想知道是否可以" in local
                modality = "inquiry" if local_inquiry else "deny" if denied else "reauthorize" if explicit else "command" if command else "mention"
                events.append(IntentEvent(
                    span=(segment_match.start() + cjk_match.start(), segment_match.start() + cjk_match.end()),
                    segment=segment,
                    action=action,
                    context=chinese_occurrence_has_git_context(action, local) or (
                        denied and not re.search(r"(?:数据库|db|事务|按钮)", local, re.IGNORECASE)
                    ),
                    modality=modality,
                    owner="delivery",
                ))
        if has_delivery_diagnostic(segment):
            events.append(IntentEvent((segment_match.start(), segment_match.end()), segment, "diagnostic", True, "command", "delivery"))
    if has_delivery_diagnostic(query):
        events.append(IntentEvent((0, len(query)), query, "diagnostic", True, "command", "delivery"))
    ordered = tuple(sorted(events, key=lambda event: event.span))
    active: set[str] = set()
    pr_requested = False
    publishing_seen = False
    pending_pr_opens = 0
    blocked = False
    barrier_exceptions: set[str] = set()
    for event in ordered:
        if event.modality == "barrier":
            blocked = True
            active.clear()
        elif event.modality == "revoke":
            if event.action == "revoke":
                active.clear()
                pr_requested = False
                barrier_exceptions.clear()
            else:
                active.discard(event.action.split(":", 1)[1])
        elif event.owner == "publishing":
            if event.action == "pr-open":
                pending_pr_opens += 1
                pr_requested = True
            elif event.action in {"pr-close", "pr-cancel-mutation", "pr-mutation"}:
                publishing_seen = True
            if event.action == "pr-cancel-pending":
                pending_pr_opens = max(0, pending_pr_opens - 1)
                pr_requested = pending_pr_opens > 0
        elif event.modality == "deny" and event.context:
            active.discard(event.action)
        elif event.modality in {"command", "reauthorize"} and event.context:
            if not blocked:
                active.add(event.action)
            elif event.modality == "reauthorize":
                barrier_exceptions.add(event.action)
                active.add(event.action)
    # Invariant: delivery requires a surviving command occurrence with local Git context.
    authorized = bool(active and (not blocked or active & barrier_exceptions) and not pr_requested and not publishing_seen)
    return DeliveryIntent(ordered, barrier, pr_requested, authorized)


def has_delivery_diagnostic(query: str) -> bool:
    """Recognize an affirmative Git divergence diagnosis, not advice or a revoked command."""
    return bool(
        DELIVERY_DIAGNOSTIC_RE.search(query)
        and not DIAGNOSTIC_DENIAL_RE.search(query)
        and not REVOCATION_RE.search(query)
    )


def has_authorized_delivery_action(query: str) -> bool:
    """Return whether a query explicitly permits at least one Git delivery action."""
    return parse_delivery_intent(query).authorized


CLAUSE_SPLIT_RE = re.compile(r"(?:[.;,，；。]|\b(?:then|but|while)\b|随后|然后)", re.IGNORECASE)
NEGATED_CLAUSE_RE = re.compile(
    r"^\s*(?:do\s+not\b|don't\b|never\b|avoid\b|skip\b|without\b|不要|不再|禁止|避免)",
    re.IGNORECASE,
)
IMPLEMENTATION_RE = re.compile(
    r"\b(?:implement|change|modify|fix|wire|build|create|update|edit|refactor)\b|"
    r"(?:实现|修改|修复|接入|开发|更新|编辑|重构)",
    re.IGNORECASE,
)
AUDIT_RE = re.compile(r"\b(?:audit|review|inspect|assess)\b|(?:审计|审查|检查|评估)", re.IGNORECASE)
STACK_OWNER = {
    "rust": {"dev-rust", "audit-rust"},
    "java": {"dev-java", "audit-java"},
    "frontend": {"dev-frontend", "audit-frontend"},
}
OWNER_ALIASES = {
    "ui-spec": {"ui specification"},
    "product-spec": {"product specification"},
}


def query_clauses(query: str) -> list[str]:
    """Split a composite request into current-action clauses."""
    return [part.strip() for part in CLAUSE_SPLIT_RE.split(query) if part.strip()]


def task_stack(query: str) -> str | None:
    """Return an explicit implementation/audit stack when the request names one."""
    affirmative = "; ".join(
        clause for clause in query_clauses(query) if not NEGATED_CLAUSE_RE.match(clause)
    )
    normalized = normalize(affirmative)
    tokens = set(normalized.split())
    if tokens & {"rust", "cargo", "tokio", "tauri"}:
        return "rust"
    if tokens & {"java", "spring", "maven", "gradle"}:
        return "java"
    if tokens & {"frontend", "react", "vue", "css", "typescript", "javascript"}:
        return "frontend"
    return None


def primary_action(query: str) -> str | None:
    """Classify the earliest affirmative implementation or audit action."""
    affirmative = "; ".join(
        clause for clause in query_clauses(query) if not NEGATED_CLAUSE_RE.match(clause)
    )
    implementation = IMPLEMENTATION_RE.search(affirmative)
    audit = AUDIT_RE.search(affirmative)
    if implementation and (not audit or implementation.start() < audit.start()):
        return "implementation"
    if audit:
        return "audit"
    return None


def exclusion_match(entry: dict[str, object], query: str) -> str | None:
    """Return the first machine-readable exclusion that owns the query boundary.

    Exclusions are exact normalized phrases. Token-set matching is deliberately
    avoided because it erased owners when the same words appeared in a different
    clause or order.
    """
    normalized_query = normalize(query)
    for raw_exclusion in entry.get("excludes", []):
        exclusion = normalize(str(raw_exclusion))
        if not exclusion:
            continue
        if exclusion in normalized_query:
            return str(raw_exclusion)
    return None


def explicit_source_request(entry: dict[str, object], query: str) -> bool:
    """Preserve a domain-matched writer in a composite audit/spec request."""
    if entry.get("mutation_class") != "source-write" or primary_action(query) != "implementation":
        return False
    stack = task_stack(query)
    return stack is not None and str(entry.get("name")) in STACK_OWNER[stack]


def owner_explicitly_negated(entry: dict[str, object], query: str) -> bool:
    """Reject an owner explicitly denied with ``don't want`` or ``without``."""
    aliases = {str(entry.get("name", "")).replace("-", " ")}
    aliases.update(OWNER_ALIASES.get(str(entry.get("name", "")), set()))
    aliases.update(
        str(keyword)
        for keyword in entry.get("keywords", [])
        if 2 <= len(normalize(str(keyword)).split()) <= 4
    )
    for alias in aliases:
        normalized_alias = normalize(alias)
        if not normalized_alias:
            continue
        target = r"\s+".join(re.escape(token) for token in normalized_alias.split())
        if re.search(
            rf"(?:\bdo\s+not\b|\bdon't\b|\bwithout\b|\bavoid(?:ing)?\b|\bskip(?:ping)?\b)"
            rf"(?:\s+\w+){{0,3}}\s+(?:a\s+|an\s+|the\s+)?{target}\b",
            query,
            re.IGNORECASE,
        ):
            return True
    return False


def _implementation_candidates(results: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return scored source-writing owners in deterministic score/name order."""
    return [
        result
        for result in results
        if result.get("mutation_class") == "source-write"
    ]


def score_entry(entry: dict[str, object], query: str) -> tuple[int, list[str]]:
    normalized_query = normalize(query)
    query_tokens = set(normalized_query.split())
    weighted_fields = (
        ("name", [str(entry["name"])], 6),
        ("intent", list(entry["intents"]), 4),
        ("keyword", list(entry["keywords"]), 3),
        ("category", [str(entry["category"])], 2),
    )
    score = 0
    reasons: list[str] = []
    for label, values, weight in weighted_fields:
        normalized_values = [(str(value), normalize(str(value))) for value in values]
        field_tokens = {
            token for _, normalized_value in normalized_values for token in normalized_value.split()
        }
        overlap = query_tokens & field_tokens
        phrase_matches = [
            value
            for value, normalized_value in normalized_values
            if normalized_query
            and (
                normalized_query in normalized_value
                or (contains_cjk(normalized_value) and normalized_value in normalized_query)
            )
        ]
        if label == "name" and not phrase_matches:
            field_score = 0
        elif phrase_matches:
            field_score = weight * max(2, len(overlap))
        else:
            field_score = weight * len(overlap)
        score += field_score
        if not field_score:
            continue
        if phrase_matches:
            reason_values = set(phrase_matches)
        else:
            reason_values = {
                value
                for value, normalized_value in normalized_values
                if query_tokens & set(normalized_value.split())
            }
        for value, normalized_value in normalized_values:
            if value in reason_values:
                reasons.append(f"{label}: {value}")
    return score, reasons


def score_query_entry(entry: dict[str, object], query: str) -> tuple[int, list[str]]:
    """Score affirmative clauses only, so denied work cannot become an owner."""
    clauses = query_clauses(query)
    denied = [clause for clause in clauses if NEGATED_CLAUSE_RE.match(clause)]
    if not denied:
        return score_entry(entry, query)
    affirmative = [clause for clause in clauses if not NEGATED_CLAUSE_RE.match(clause)]
    if not affirmative:
        return 0, []
    score, reasons = score_entry(entry, "; ".join(affirmative))
    denied_score = max(score_entry(entry, clause)[0] for clause in denied)
    return (0, []) if denied_score >= score else (score, reasons)


def search(index: dict[str, object], query: str) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    stack = task_stack(query)
    action = primary_action(query)
    for raw_entry in index["skills"]:
        entry = dict(raw_entry)
        entry_name = str(entry["name"])
        if stack and entry_name in set().union(*STACK_OWNER.values()) and entry_name not in STACK_OWNER[stack]:
            continue
        authorized_delivery = (
            entry["name"] == "repo-delivery" and has_authorized_delivery_action(query)
        )
        if entry["name"] == "repo-delivery" and not authorized_delivery:
            continue
        if not authorized_delivery and owner_explicitly_negated(entry, query):
            continue
        excluded_by = exclusion_match(entry, query)
        # An explicit authorized Git action remains a valid handoff target for a
        # composite implementation request. The implementation owner's exclusion
        # must not erase the separate delivery owner from the plan.
        if excluded_by and not authorized_delivery and not explicit_source_request(entry, query):
            continue
        score, reasons = score_query_entry(entry, query)
        if stack and entry_name in STACK_OWNER[stack]:
            if action == "implementation" and entry_name.startswith("dev-"):
                score += 50
                reasons.append(f"explicit {stack} implementation owner")
            elif action == "audit" and entry_name.startswith("audit-"):
                score += 50
                reasons.append(f"explicit {stack} audit owner")
        if authorized_delivery:
            # Structured intent is a stronger routing contract than incidental
            # discovery-token overlap (for example ``git fetch --prune origin``).
            score += 100
            reasons.append("authorized delivery action")
        if score:
            results.append(
                {
                    "name": entry["name"],
                    "category": entry["category"],
                    "score": score,
                    "matched": reasons,
                    "excludes": entry["excludes"],
                    "related": entry["related"],
                    "owner": entry.get("owner", entry["name"]),
                    "mutation_class": entry.get("mutation_class"),
                    "required_capabilities": entry.get("required_capabilities", []),
                    "allowed_effects": entry.get("allowed_effects", []),
                    "forbidden_effects": entry.get("forbidden_effects", []),
                    "stop_states": entry.get("stop_states", []),
                }
            )
    ordered = sorted(results, key=lambda item: (-int(item["score"]), str(item["name"])))
    delivery = next((item for item in ordered if item["name"] == "repo-delivery"), None)
    implementations = _implementation_candidates(ordered)
    if delivery is not None and implementations:
        primary = implementations[0]
        owner_chain = [str(primary["owner"]), "repo-delivery"]
        handoff = {
            "owners": owner_chain,
            "primary_owner": str(primary["owner"]),
            "handoff_owner": "repo-delivery",
            "authorization_required": True,
            "reason": "source implementation completes before separately authorized Git delivery",
        }
        # Keep the historical delivery-first ordering for pure delivery callers,
        # while exposing a deterministic composite owner chain to machine clients.
        delivery["owner_chain"] = owner_chain
        delivery["handoff"] = handoff
        delivery["plan"] = owner_chain
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="Task or capability to search for")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to print")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    query = " ".join(args.query)
    results = search(load_index(repo_root()), query)[: args.limit]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    if not results:
        print("No matching Skill found.")
        return 1
    for result in results:
        matched = "; ".join(result["matched"][:2])
        print(f"{result['name']}\t{result['score']}\t{result['category']}\t{matched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
