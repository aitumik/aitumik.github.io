---
title: "Building a Dropdown component"
date: 2023-08-28T17:14:01+03:00
draft: true
---

# Introduction

We are going to create a component that is extendable and accepts the interface below

```ts
export interface DropdownProps {
    selectedItems: any[]
    options: any[]
    onChange: any
}
```

```html
<div className="container">
    <div>
        <label>Multi Select</label>
        <button>Toggle</button>
        <li>
            <li>option 1</li>
            <li>option 2</li>
            ....
        </ul>
    </div>
</div>
```
