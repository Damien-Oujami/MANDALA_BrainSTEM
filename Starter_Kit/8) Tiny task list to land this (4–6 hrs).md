 - Apply SQL migration to Neon/Supabase.

 - Run FastAPI app (uvicorn app.main:app --reload).

 - Run worker (python workers/loop_worker.py).

 - Fire seed events; verify profile endpoint + Redis warming.

 - Add encryption-at-rest for raw_text (libsodium or pgp_sym_encrypt).

 - (Optional) Docker-compose for pg/redis/api/worker.
