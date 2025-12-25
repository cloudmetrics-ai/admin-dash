# Component Documentation

Complete reference for all reusable UI components.

---

## Input Component

Styled input field with label, error message, and helper text support.

### Import

```tsx
import Input from '@/components/ui/Input';
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | Label text displayed above input |
| `error` | `string` | - | Error message displayed below input |
| `helperText` | `string` | - | Helper text displayed below input |
| All standard HTML input props | - | - | type, placeholder, value, onChange, etc. |

### Usage

```tsx
<Input
  type="email"
  label="Email"
  placeholder="you@example.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={emailError}
  required
/>
```

---

## Button Component

Button with primary/secondary variants and loading state.

### Import

```tsx
import Button from '@/components/ui/Button';
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary'` | `'primary'` | Button style variant |
| `loading` | `boolean` | `false` | Shows loading spinner |
| `children` | `ReactNode` | - | Button content |
| All standard HTML button props | - | - | onClick, disabled, type, etc. |

### Usage

```tsx
// Primary button
<Button onClick={handleSubmit} loading={isLoading}>
  Submit
</Button>

// Secondary button
<Button variant="secondary" onClick={handleCancel}>
  Cancel
</Button>
```

---

## Checkbox Component

Styled checkbox with label support.

### Import

```tsx
import Checkbox from '@/components/ui/Checkbox';
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | Label text next to checkbox |
| All standard HTML input props | - | - | checked, onChange, etc. |

### Usage

```tsx
<Checkbox
  label="Remember me"
  checked={rememberMe}
  onChange={(e) => setRememberMe(e.target.checked)}
/>
```

---

## Logo Component

Reusable logo with icon and optional text.

### Import

```tsx
import Logo from '@/components/ui/Logo';
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showText` | `boolean` | `true` | Show "Welcome Back" text |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Logo size |

### Usage

```tsx
// Full logo with text
<Logo />

// Icon only
<Logo showText={false} />

// Large size
<Logo size="lg" />
```

---

## AuthLayout Component

Layout wrapper for authentication pages (login, register).

### Import

```tsx
import AuthLayout from '@/components/layouts/AuthLayout';
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Page content |

### Usage

```tsx
export default function LoginPage() {
  return (
    <AuthLayout>
      <Logo />
      <form>
        {/* Your form content */}
      </form>
    </AuthLayout>
  );
}
```

---

## Styling Components

All components use the design system CSS variables. You can customize them using inline styles or CSS classes.

### Example: Custom Styling

```tsx
<Button
  style={{
    maxWidth: '200px',
    marginTop: 'var(--spacing-lg)',
  }}
>
  Custom Button
</Button>
```

---

## Accessibility

All components follow accessibility best practices:

- ✅ Proper ARIA labels
- ✅ Keyboard navigation support
- ✅ Focus visible states
- ✅ Semantic HTML elements

---

## Creating New Components

When creating new components, follow these guidelines:

1. **Use TypeScript** - Define proper interfaces for props
2. **Use Design System** - Always use CSS variables
3. **Add Documentation** - Update this file with usage examples
4. **Make it Reusable** - Accept props for customization
5. **Follow Naming** - Use PascalCase for component names

### Template

```tsx
/**
 * MyComponent
 * ===========
 * 
 * Brief description of what this component does.
 */

import React from 'react';

export interface MyComponentProps {
  // Define your props
  title: string;
  onClick?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  title,
  onClick,
}) => {
  return (
    <div
      style={{
        padding: 'var(--spacing-md)',
        background: 'var(--color-background)',
      }}
      onClick={onClick}
    >
      <h2 style={{ color: 'var(--color-text-primary)' }}>
        {title}
      </h2>
    </div>
  );
};

export default MyComponent;
```

---

**For more information, see [FRONTEND_GUIDE.md](./FRONTEND_GUIDE.md)**
