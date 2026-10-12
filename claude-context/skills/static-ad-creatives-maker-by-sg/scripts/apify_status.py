"""Read-only, free: show the Apify plan, the billing cycle, usage so far and the monthly usage limit, so the budget is known before any pull.
Run at the start of Stage 2:  python scripts/apify_status.py
Rules: never raise the usage limit without Soumil's word (he said so on 2026-10-09); prepaid credit expires at the end of the cycle, so unused credit is not saved.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apify_lib as A

me = A._req('GET', 'users/me').get('data') or {}
plan = me.get('plan') or {}
lim = (A._req('GET', 'users/me/limits').get('data') or {})
used = (lim.get('current') or {}).get('monthlyUsageUsd') or 0.0
limit = (lim.get('limits') or {}).get('maxMonthlyUsageUsd')
cyc = lim.get('monthlyUsageCycle') or {}
print('plan: %s | base price $%s a month | prepaid usage credit $%s' % (plan.get('id'), plan.get('monthlyBasePriceUsd'), plan.get('monthlyUsageCreditsUsd')))
print('billing cycle: %s to %s (credit expires at the end of the cycle)' % ((cyc.get('startAt') or '')[:10], (cyc.get('endAt') or '')[:10]))
print('usage so far this cycle: $%.2f of the $%s monthly usage limit | room left: $%.2f' % (used, limit, (limit or 0) - used))
print('billing lags about a minute after a run ends, so re-read before a big pull.')
