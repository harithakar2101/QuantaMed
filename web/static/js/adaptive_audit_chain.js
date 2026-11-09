/**
 * LensCode – Adaptive QuantaMed
 * Cryptographic Hash-Chained Audit Ledger & Verification Engine (Phase 2)
 */

(function (window) {
  'use strict';

  const STORAGE_KEY = 'quantamed_audit_chain_v2';

  class AuditChain {
    constructor() {
      this.chain = this.loadChain();
      if (this.chain.length === 0) {
        this.createGenesisBlock();
      }
    }

    async computeSHA256(text) {
      const msgBuffer = new TextEncoder().encode(text);
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    createGenesisBlock() {
      const genesis = {
        index: 0,
        timestamp: "2026-11-01T00:00:00Z",
        actor: "SYSTEM",
        role: "System Genesis",
        action: "GENESIS_BLOCK",
        payload: { message: "LensCode Adaptive QuantaMed Immutable Audit Ledger Initialized" },
        previousHash: "0000000000000000000000000000000000000000000000000000000000000000",
        hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      };
      this.chain = [genesis];
      this.saveChain();
    }

    async log(action, actor, role, payload = {}) {
      const previousBlock = this.chain[this.chain.length - 1];
      const index = this.chain.length;
      const timestamp = new Date().toISOString();

      const rawContent = `${index}|${timestamp}|${actor}|${role}|${action}|${JSON.stringify(payload)}|${previousBlock.hash}`;
      const hash = await this.computeSHA256(rawContent);

      const newBlock = {
        index,
        timestamp,
        actor,
        role,
        action,
        payload,
        previousHash: previousBlock.hash,
        hash
      };

      this.chain.push(newBlock);
      this.saveChain();

      if (window.QuantaMedStore) {
        window.QuantaMedStore.set('auditLog', [...this.chain]);
      }

      return newBlock;
    }

    /**
     * Cryptographically verifies every link in the entire audit chain
     */
    async verifyChain() {
      for (let i = 1; i < this.chain.length; i++) {
        const current = this.chain[i];
        const previous = this.chain[i - 1];

        // 1. Verify previous hash pointer
        if (current.previousHash !== previous.hash) {
          return {
            isChainValid: false,
            brokenBlockIndex: i,
            reason: `Broken chain link at Block #${i}: previousHash mismatch.`,
            totalBlocks: this.chain.length
          };
        }

        // 2. Recompute current block hash
        const rawContent = `${current.index}|${current.timestamp}|${current.actor}|${current.role}|${current.action}|${JSON.stringify(current.payload)}|${current.previousHash}`;
        const recomputed = await this.computeSHA256(rawContent);
        if (recomputed !== current.hash) {
          return {
            isChainValid: false,
            brokenBlockIndex: i,
            reason: `Tampered payload at Block #${i}: hash digest mismatch.`,
            totalBlocks: this.chain.length
          };
        }
      }

      return {
        isChainValid: true,
        brokenBlockIndex: null,
        totalBlocks: this.chain.length,
        verifiedAt: new Date().toISOString(),
        latestHash: this.chain[this.chain.length - 1].hash
      };
    }

    getChain() {
      return [...this.chain];
    }

    saveChain() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.chain));
      } catch (e) {
        console.warn("Could not persist audit chain to localStorage:", e);
      }
    }

    loadChain() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) return JSON.parse(raw);
      } catch (e) { }
      return [];
    }
  }

  window.AdaptiveAuditChain = new AuditChain();

})(window);
