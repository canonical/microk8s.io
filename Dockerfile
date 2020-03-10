# syntax=docker/dockerfile:experimental

# Build stage: Install ruby dependencies
# ===
FROM ruby:2.5 AS build-site
WORKDIR /srv
ADD . .
RUN bundle install
RUN bundle exec jekyll build

# Build stage: Install yarn dependencies
# ===
FROM node:12-slim AS yarn-dependencies
WORKDIR /srv
ADD package.json .
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn yarn install

# Build stage: Run "yarn run build-js"
# ===
FROM yarn-dependencies AS build-js
WORKDIR /srv
COPY . .
RUN yarn run build-js

# Build stage: Run "yarn run build-css"
# ===
FROM yarn-dependencies AS build-css
WORKDIR /srv
COPY . .
RUN yarn run build-css

# Build the production image
# ===
FROM ubuntu:focal

# Set up environment
ENV LANG C.UTF-8
WORKDIR /srv

# Install nginx
RUN apt-get update && apt-get install --no-install-recommends --yes nginx

# Import code, build assets and mirror list
RUN rm -rf package.json yarn.lock .babelrc webpack.config.js Gemfile.lock nginx.conf
COPY --from=build-site srv/_site .
COPY --from=build-css srv/css css
COPY --from=build-js srv/js js

ARG BUILD_ID
ADD nginx.conf /etc/nginx/sites-enabled/default
RUN sed -i "s/~BUILD_ID~/${BUILD_ID}/" /etc/nginx/sites-enabled/default

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]

