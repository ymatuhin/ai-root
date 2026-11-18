# Mocking at Boundaries

Mock only true external dependencies (third-party APIs, clock/randomness, unowned services) via injected ports; for owned code and local-substitutable stores, test through real implementations or in-memory adapters as defined in [codebase-design/DEEPENING.md](../codebase-design/DEEPENING.md).

## Prefer SDK-style interfaces over generic fetchers

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint
