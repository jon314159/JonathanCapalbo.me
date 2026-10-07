# React browser assets

Pinned React and ReactDOM 18.3.1 production UMD assets, copied as static browser files without a package installation. Both use the MIT license in `LICENSE`.

Sources:

- https://unpkg.com/react@18.3.1/umd/react.production.min.js
- https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js
- https://unpkg.com/react@18.3.1/LICENSE

The website serves these files locally; it makes no runtime CDN request for React. The explorer uses ReactDOM `createRoot` and React `createElement`, so no transpilation is needed.
