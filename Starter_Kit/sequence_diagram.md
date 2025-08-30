sequenceDiagram
    autonumber
    %% === Actors / Services ===
    actor U as User / Device
    participant Z as Zodiac Companion Runtime (per user)
    participant WH as Brainstem Ingest Webhook
    participant GW as API Gateway + Auth
    participant Q as Event Queue (SQS/Kafka)
    participant W as Worker(s)
    participant IDEM as Idempotency Store
    participant DB as Event Store / Features DB
    participant NOTIF as Notifier (Email/Slack/Webhooks)
    participant SCH as Morgan Scheduler
    participant RL as Rate Limiter (Token Bucket)
    participant P as Provider APIs (Zodiac/3rd party)

    %% === PUSH PATH (webhooks first-class) ===
    U->>Z: user action / state change
    Z->>WH: POST /ingest {event}+signature
    WH->>GW: verify HMAC + auth
    GW->>Q: enqueue normalized event
    Note right of Q: durable + backpressure-friendly
    Q->>W: deliver message
    W->>IDEM: check idempotency key
    alt duplicate event
        W-->>Q: ack & drop
    else new event
        W->>DB: persist event + derived features
        opt fan-out
            W->>NOTIF: notify stakeholders / downstream hooks
        end
    end

    %% === PULL PATH (safety net sweeps) ===
    SCH->>RL: shard tick (+ jitter)
    RL-->>SCH: tokens?
    alt tokens available
        SCH->>P: GET /events?since=cursor&page=1
        P-->>SCH: 200 OK + events + nextCursor
        SCH->>Q: enqueue each event
        SCH->>SCH: update cursor
    else rate limited
        RL-->>SCH: wait / backoff
    end

    %% === ERROR HANDLING HINTS ===
    alt 401/403 at GW
        GW-->>Z: reject (bad/missing signature)
    else 429/5xx downstream
        W-->>Q: requeue with exponential backoff + jitter
    end
