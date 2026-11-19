# NOTE: webpack 4 runs on node - bun is the package manager only
FROM node:22-slim

COPY --from=oven/bun:1 /usr/local/bin/bun /usr/local/bin/bun

WORKDIR /app/

ENV PORT=3000

COPY \
  package.json \
  bun.lock \
  ./

RUN bun install --frozen-lockfile

COPY \
  webpack.config.js \
  postcss.config.js \
  .babelrc \
  .stylelintrc.js \
  .eslintrc.js \
  .eslintignore \
  ./
COPY obp_ui/ ./obp_ui/

EXPOSE 3000

CMD ["sh", "-c", "exec bun run dev --port ${PORT}"]
