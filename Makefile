FRONTEND_DIR=apps/frontend
BACKEND_DIR=apps/backend

.PHONY: dev be fe test fmt

dev:
cd $(BACKEND_DIR) && python -m uvicorn app.main:app --reload & \
BACKEND_PID=$$!; \
cd $(FRONTEND_DIR) && npm install && npm run dev; \
kill $$BACKEND_PID || true

be:
cd $(BACKEND_DIR) && python -m uvicorn app.main:app --reload

fe:
cd $(FRONTEND_DIR) && npm install && npm run dev

test:
cd $(BACKEND_DIR) && pytest
cd $(FRONTEND_DIR) && npm install && npm run test

fmt:
cd $(BACKEND_DIR) && make fmt
cd $(FRONTEND_DIR) && npm install && npm run fmt
