# Agent 2: Deployment Checklist

**Complete production readiness checklist for Agent 2 - SRS → Diagrams pipeline**

---

## Pre-Deployment (Development)

- [ ] **Code Review**
  - [ ] All Python files pass syntax checks
  - [ ] No unused imports
  - [ ] Error handling covers all paths
  - [ ] Code follows PEP 8 style guide

- [ ] **Environment Setup**
  - [ ] `.env` file created from `.env.example`
  - [ ] `ANTHROPIC_API_KEY` is valid and active
  - [ ] Python 3.13 installed
  - [ ] Virtual environment created and activated

- [ ] **Dependencies**
  - [ ] `pip install -r requirements.txt` succeeds
  - [ ] OR `pipenv install` succeeds
  - [ ] No conflicting package versions
  - [ ] All imports work without errors

- [ ] **Local Testing**
  - [ ] Server starts: `python -m uvicorn app:app --reload`
  - [ ] Health check passes: `curl http://localhost:8000/health`
  - [ ] API docs accessible: `http://localhost:8000/docs`
  - [ ] Test endpoint succeeds: `test_agent2.py` runs without errors
  - [ ] All 6 diagrams generate correctly
  - [ ] Image URLs are valid

- [ ] **File Validation**
  - [ ] `srs.json` is valid and complete
  - [ ] `diagrams_viewer.html` renders correctly
  - [ ] All required Python files exist and are readable

---

## Docker Preparation

- [ ] **Docker Setup**
  - [ ] Docker installed and running
  - [ ] `Dockerfile` is present and syntactically correct
  - [ ] `docker-compose.yml` is present and valid
  - [ ] `.dockerignore` created (optional but recommended)

- [ ] **Docker Build**
  - [ ] Image builds successfully: `docker build -t diagram-generator:latest .`
  - [ ] Image size is reasonable (< 1GB)
  - [ ] No warnings during build
  - [ ] Layer caching is optimized

- [ ] **Docker Test**
  - [ ] Container runs: `docker run -p 8000:8000 diagram-generator:latest`
  - [ ] Health check works: `curl http://localhost:8000/health`
  - [ ] Logs are clean and informative
  - [ ] Container stops gracefully: `docker stop <container-id>`

---

## Security Checklist

- [ ] **Secrets Management**
  - [ ] `.env` file added to `.gitignore`
  - [ ] API key never hardcoded in source
  - [ ] No API keys in git history
  - [ ] Use AWS Secrets Manager / Azure KeyVault in production

- [ ] **Access Control**
  - [ ] CORS settings reviewed and locked down (currently open to all origins)
  - [ ] Authentication disabled for testing, but consider adding for production
  - [ ] Input validation in place (Pydantic models)
  - [ ] Rate limiting considered (add in production)

- [ ] **Data Security**
  - [ ] No sensitive data in SRS logs
  - [ ] API responses don't expose internal structure
  - [ ] Error messages don't leak system information

- [ ] **Network Security**
  - [ ] HTTPS required in production (use nginx/load balancer)
  - [ ] Firewall rules restrict traffic to needed ports
  - [ ] No unnecessary open ports

---

## Performance & Scalability

- [ ] **Performance Testing**
  - [ ] Response time acceptable for single request (< 30s)
  - [ ] Memory usage stable (no memory leaks)
  - [ ] CPU usage reasonable
  - [ ] Concurrent requests handled correctly

- [ ] **Load Testing**
  - [ ] Can handle 10 concurrent requests
  - [ ] Can handle 100 concurrent requests
  - [ ] Graceful degradation under load
  - [ ] No timeouts or dropped connections

- [ ] **Optimization**
  - [ ] Database queries optimized (if applicable)
  - [ ] API response times logged
  - [ ] Bottlenecks identified and addressed
  - [ ] Caching strategy implemented (optional)

---

## Monitoring & Logging

- [ ] **Logging Setup**
  - [ ] Logs written to file, not just stdout
  - [ ] Log rotation configured
  - [ ] Debug logging disabled in production
  - [ ] Log format includes timestamp, level, message

- [ ] **Error Tracking**
  - [ ] All exceptions caught and logged
  - [ ] Error messages are helpful and actionable
  - [ ] Stack traces logged but not exposed to users
  - [ ] Integration with monitoring service (Sentry, etc.)

- [ ] **Health Checks**
  - [ ] `/health` endpoint responds correctly
  - [ ] Liveness probe configured
  - [ ] Readiness probe configured
  - [ ] Metrics exposed (Prometheus format recommended)

---

## Integration Testing

- [ ] **Agent 1 Compatibility**
  - [ ] API contract matches specification
  - [ ] Request/response formats correct
  - [ ] Error handling matches expectations
  - [ ] Integration test passes with sample Agent 1 output

- [ ] **End-to-End Testing**
  - [ ] Transcript → SRS → Diagrams workflow complete
  - [ ] All 6 diagram types generate correctly
  - [ ] Image URLs display properly
  - [ ] No data loss between agents

- [ ] **Backward Compatibility**
  - [ ] Old SRS format still works (if applicable)
  - [ ] Deprecated endpoints handled gracefully

---

## Database/Storage (if applicable)

- [ ] **Data Persistence**
  - [ ] Generated diagrams saved successfully
  - [ ] No data corruption on restart
  - [ ] Backup strategy defined
  - [ ] Recovery procedure tested

- [ ] **Storage Validation**
  - [ ] Disk space requirements calculated
  - [ ] Storage scaling plan in place
  - [ ] Cleanup of old diagrams implemented

---

## Documentation

- [ ] **README**
  - [ ] Setup instructions clear
  - [ ] Dependencies listed
  - [ ] Example requests/responses provided
  - [ ] Troubleshooting section included

- [ ] **Deployment Guide**
  - [ ] Docker setup documented
  - [ ] Environment variables explained
  - [ ] Port configuration clear
  - [ ] Monitoring setup instructions included

- [ ] **Integration Guide**
  - [ ] API contract fully documented
  - [ ] SRS schema clearly defined
  - [ ] Error codes and meanings listed
  - [ ] Integration examples provided

- [ ] **Code Documentation**
  - [ ] All functions have docstrings
  - [ ] Complex logic has inline comments
  - [ ] Architecture decisions documented

---

## Deployment Process

### Development → Staging

- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Staging deployment successful
- [ ] Smoke tests passing on staging
- [ ] Performance acceptable on staging

### Staging → Production

- [ ] Backup created before deployment
- [ ] Rollback plan documented
- [ ] Maintenance window scheduled (if needed)
- [ ] On-call team briefed
- [ ] Deployment scripts tested
- [ ] Health monitoring verified

### Post-Deployment

- [ ] All services responding
- [ ] No errors in logs
- [ ] Metrics normal
- [ ] Integration working with Agent 1
- [ ] User acceptance testing complete
- [ ] Performance monitored for 24 hours

---

## Production Monitoring

- [ ] **Daily Checks**
  - [ ] Server health: Status code 200
  - [ ] Error rate < 0.1%
  - [ ] Average response time < 5s
  - [ ] No disk space issues
  - [ ] API key not expired

- [ ] **Weekly Checks**
  - [ ] Review logs for patterns
  - [ ] Check backup integrity
  - [ ] Verify security patches available
  - [ ] Capacity planning review

- [ ] **Monthly Checks**
  - [ ] Disaster recovery drill
  - [ ] Performance trend analysis
  - [ ] Cost analysis
  - [ ] Security audit

---

## Troubleshooting Runbook

### Issue: High Response Times

**Symptoms:** Requests taking > 10 seconds

**Steps:**
1. Check Claude API status: https://status.anthropic.com/
2. Check network latency: `ping api.anthropic.com`
3. Review logs for timeout errors
4. Check server CPU/memory usage
5. Reduce SRS complexity for testing

**Mitigation:**
- Increase timeout values
- Implement caching layer
- Scale horizontally with load balancer

### Issue: Authentication Failures

**Symptoms:** "ANTHROPIC_API_KEY not set" or "Unauthorized"

**Steps:**
1. Verify `.env` file exists
2. Check API key is valid: `curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/models`
3. Ensure key hasn't expired
4. Generate new key if needed

**Mitigation:**
- Use secrets manager instead of .env
- Implement key rotation policy

### Issue: Diagram Generation Failures

**Symptoms:** 500 error, invalid Mermaid syntax

**Steps:**
1. Check Claude response format
2. Validate SRS schema
3. Review error logs
4. Test with sample SRS

**Mitigation:**
- Add retry logic with exponential backoff
- Improve Claude prompt for robustness
- Add more detailed error messages

### Issue: Memory Leaks

**Symptoms:** Memory usage increases over time

**Steps:**
1. Check for unclosed file handles
2. Monitor Python garbage collection
3. Use memory profiler: `python -m memory_profiler app.py`
4. Check for circular references

**Mitigation:**
- Implement periodic restart (no downtime with load balancer)
- Add resource cleanup in finally blocks
- Use context managers for file operations

---

## Rollback Plan

If deployment fails:

1. **Immediate Rollback** (within 1 hour)
   - Stop the new container
   - Restore from previous Docker image
   - Update DNS/load balancer if needed
   - Verify health checks pass

2. **Communication**
   - Notify team of rollback
   - Post incident summary
   - Update status page

3. **Investigation**
   - Review logs from failed deployment
   - Identify root cause
   - Document fix

4. **Retry**
   - Apply fixes
   - Re-test locally and in staging
   - Deploy again with monitoring

---

## Sign-Off Checklist

Before going to production:

- [ ] **Development Lead:** Code quality approved
- [ ] **Security Officer:** Security review passed
- [ ] **DevOps:** Deployment readiness confirmed
- [ ] **QA:** Testing complete and passed
- [ ] **Project Manager:** Timeline and requirements met

---

## Go/No-Go Decision

**GO to Production:** If all items checked ✅  
**NO-GO:** If any critical items unchecked ❌

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial production release |

---

**Last Updated:** 2024  
**Next Review:** After production deployment  
**Owner:** DevOps Team
