.PHONY: test lint fmt up down argocd-password

TF := terraform -chdir=infra/terraform
export KUBECONFIG := $(CURDIR)/infra/terraform/kubeconfig

test:
	cd app && uv run pytest

lint:
	cd app && uv run ruff check . && uv run ruff format --check .

fmt:
	cd app && uv run ruff format . && uv run ruff check --fix .

up:
	$(TF) init && $(TF) apply -auto-approve

down:
	$(TF) destroy -auto-approve

argocd-password:
	@kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
