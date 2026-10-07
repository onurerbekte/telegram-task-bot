import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from bot import handler_for, build_application
from store import TaskStore


def invoke(store,command,args=(),user=1,chat="private"):
    reply=AsyncMock()
    update=SimpleNamespace(effective_user=SimpleNamespace(id=user),effective_chat=SimpleNamespace(type=chat),effective_message=SimpleNamespace(reply_text=reply))
    asyncio.run(handler_for(store,command)(update,SimpleNamespace(args=list(args))))
    return reply.call_args.args[0]


def test_commands_and_language(tmp_path):
    store=TaskStore(tmp_path/"test.sqlite")
    assert "Henüz" in invoke(store,"list")
    assert "#1" in invoke(store,"add",["Demo","görev"])
    assert "Demo görev" in invoke(store,"list")
    assert "English" in invoke(store,"lang",["en"])
    assert "updated" in invoke(store,"done",["1"])
    assert "✓" in invoke(store,"list")
    assert "deleted" in invoke(store,"delete",["1"])
    assert "No tasks" in invoke(store,"list")


def test_user_isolation_and_private_only(tmp_path):
    store=TaskStore(tmp_path/"test.sqlite")
    invoke(store,"add",["Only","mine"],user=1)
    assert "Henüz" in invoke(store,"list",user=2)
    assert "sana ait değil" in invoke(store,"delete",["1"],user=2)
    assert "özel" in invoke(store,"add",["Group"],chat="group")
    assert len(store.list(1))==1


def test_validation_and_persistence(tmp_path):
    path=tmp_path/"test.sqlite";store=TaskStore(path)
    assert "Geçerli" in invoke(store,"add",[])
    assert "Geçerli" in invoke(store,"add",["x"*201])
    assert "Geçerli" in invoke(store,"done",["not-id"])
    invoke(store,"add",["Saved"])
    assert TaskStore(path).list(1)[0]["title"]=="Saved"
    for _ in range(99):store.add(1,"Item")
    with pytest.raises(ValueError):store.add(1,"Over limit")


def test_sdk_application_builds_without_network(tmp_path):
    # Intentionally fake token for offline construction only; not a credential.
    application=build_application("123:fictional-demo-token",TaskStore(tmp_path/"test.sqlite"))
    assert len(application.handlers[0])==7
