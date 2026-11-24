# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**.

## Dependency categories

First check that the modules share a responsibility and that combining them reduces what callers must know without coupling unrelated changes. Dependency categories help choose a testing strategy; they do not by themselves justify merging modules.

### 1. In-process

Pure computation, in-memory state, no I/O. When the responsibilities belong together, the modules can often be combined and tested through the new interface directly, without an adapter.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). A stand-in can make the combined module practical to test if it reproduces the relevant behavior. Keep the dependency internal when callers do not need to configure or replace it.

### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam discipline

- **Justify each seam.** Production and test adapters are one useful reason for a port. A stable boundary around an external dependency can also justify one; an extra interface around an unchanging internal call may only add indirection.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

## Testing strategy: replace, don't layer

- Remove old unit tests only after checking that the new tests cover their relevant scenarios and failure cases. Keep tests that still verify a distinct responsibility or provide useful failure diagnosis.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should usually survive internal refactors when behavior and the tested interface stay the same. A changed test is a reason to inspect its coupling, not proof that it is unnecessary.
