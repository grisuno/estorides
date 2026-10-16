# `estorides_core.event_bus`

> Source: [estorides_core/event_bus.py:1](../../estorides_core/event_bus.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_core.event_bus ======================== In process publish subscribe channel for orchestrator lifecycle events.

I let metrics, SSE and future plugins observe runs without the
orchestrator importing them. Delivery is synchronous and total:
a failing subscriber never breaks a run and never mutates the
payload seen by the next subscriber.

## Contents

- **Classes:** [`EventBus`](#eventbus)
- **Functions:** [`get_bus`](#get_bus)

## Classes

<a id="eventbus"></a>

### `EventBus`

`class` | [estorides_core/event_bus.py:24](../../estorides_core/event_bus.py#L24)

```python
class EventBus
```

Synchronous in memory event channel with isolated delivery.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#eventbus-__init__) | constructor | Create an empty bus with no subscribers. |
| [`subscribe`](#eventbus-subscribe) | method | Register handler for event and return it for unsubscription. |
| [`unsubscribe`](#eventbus-unsubscribe) | method | Remove handler from event and report whether it was present. |
| [`publish`](#eventbus-publish) | method | Deliver a copy of payload to each subscriber and count attempts. |
| [`clear`](#eventbus-clear) | method | Remove subscribers for one event or for the whole bus. |
| [`subscriber_count`](#eventbus-subscriber_count) | method | Return the number of handlers registered for event. |

<a id="eventbus-__init__"></a>

#### `EventBus.__init__`

`constructor` | [estorides_core/event_bus.py:27](../../estorides_core/event_bus.py#L27)

```python
def __init__(self) -> None
```

Create an empty bus with no subscribers.

<a id="eventbus-subscribe"></a>

#### `EventBus.subscribe`

`method` | [estorides_core/event_bus.py:31](../../estorides_core/event_bus.py#L31)

```python
def subscribe(self, event: str, handler: Handler) -> Handler
```

Register handler for event and return it for unsubscription.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `str` |  |  |
| `handler` | `Handler` |  |  |

**Returns:** `Handler`

**Raises**

- `TypeError`: (raised in the body, not documented)

<a id="eventbus-unsubscribe"></a>

#### `EventBus.unsubscribe`

`method` | [estorides_core/event_bus.py:41](../../estorides_core/event_bus.py#L41)

```python
def unsubscribe(self, event: str, handler: Handler) -> bool
```

Remove handler from event and report whether it was present.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `str` |  |  |
| `handler` | `Handler` |  |  |

**Returns:** `bool`

<a id="eventbus-publish"></a>

#### `EventBus.publish`

`method` | [estorides_core/event_bus.py:50](../../estorides_core/event_bus.py#L50)

```python
def publish(self, event: str, payload: dict[str, Any]) -> int
```

Deliver a copy of payload to each subscriber and count attempts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `str` |  |  |
| `payload` | `dict[str, Any]` |  |  |

**Returns:** `int`

**Raises**

- `TypeError`: (raised in the body, not documented)

<a id="eventbus-clear"></a>

#### `EventBus.clear`

`method` | [estorides_core/event_bus.py:63](../../estorides_core/event_bus.py#L63)

```python
def clear(self, event: str | None = None) -> None
```

Remove subscribers for one event or for the whole bus.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `str \| None` | `None` |  |

<a id="eventbus-subscriber_count"></a>

#### `EventBus.subscriber_count`

`method` | [estorides_core/event_bus.py:71](../../estorides_core/event_bus.py#L71)

```python
def subscriber_count(self, event: str) -> int
```

Return the number of handlers registered for event.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `str` |  |  |

**Returns:** `int`

---

## Functions

<a id="get_bus"></a>

### `get_bus`

`function` | [estorides_core/event_bus.py:85](../../estorides_core/event_bus.py#L85)

```python
def get_bus() -> EventBus
```

Return the process wide shared bus instance.

**Returns:** `EventBus`

*Called by:* [`Orchestrator.run`](estorides_core.orchestrator.py.md#orchestrator-run)

---
