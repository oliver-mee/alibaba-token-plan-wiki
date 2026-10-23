# Current Token Plan policy notes

Evidence checked 2026-10-23 against the existing October 21 to 23 vendor captures. These current notes supersede older cycle-reset and pack-limit descriptions, not historical measurements.

## Personal subscriptions

- An upgrade does **not** reset the subscription cycle. Pay the monthly price **difference**, prorated for remaining days; the extra current-cycle Credits are the monthly quota **difference**, prorated for remaining days. The full new tier's monthly quota starts next subscription month.
- Credit Packs add **20,000 Credits per pack**, outside the monthly quota, with at most **five held simultaneously**. A valid subscription is required. Packs are valid one month, expire without rollover/refund, and are consumed after the plan allowance. Service pauses only when both plan allowance and available pack Credits are exhausted. The sales label per month is not a recurring addition to the plan quota.
- Personal is single-user only. Account/API-key sharing between people is prohibited. The same user may explicitly configure the same key on multiple devices. Resetting it invalidates the old key on all devices.
- The October 22 CN Personal supported-tool wording drops Trae and Lingma. The EN list is unchanged. This is regional documentation divergence, not a model delisting or evidence that those clients cannot connect.

## Team subscriptions

- Team concurrency is explicitly dynamic, adjusted to resource load. Published TPM/RPM are not a static promised agent/concurrency count.
- Seat downgrades are unsupported. On member removal, a seat returns to the reusable pool only if the member used zero Credits; a used seat does not return. Do not generalise an older unconditional seat-reclaim sentence to member removal.
- A shared-pack member cap can be changed only once every 24 hours and only for a seated member. Available quota is the smaller of the configured cap and organisation shared-pack balance.

## Purchase visibility

The EN overview explicitly says purchase and use are Singapore-only: switch the Model Studio console to Singapore. A hidden entry in another region is not proof of product retirement. CN remains a distinct Beijing product/authentication realm.

## Primary sources

Captured 2026-10-23, with body updates observed October 21/22:

- [EN Personal FAQ](https://www.alibabacloud.com/help/en/model-studio/token-plan-personal-faq), capture `cloud-en-token-plan-personal-faq.txt`: monthly quota and pack sections, upgrade, sharing and multiple-device answers.
- [CN Personal FAQ](https://help.aliyun.com/zh/model-studio/token-plan-personal-faq), capture `cloud-cn-token-plan-personal-faq.txt`.
- [EN overview](https://www.alibabacloud.com/help/en/model-studio/token-plan-overview), capture `cloud-en-token-plan-overview.txt`: Singapore notice, pack pricing and quota footnotes.
- [EN Team FAQ](https://www.alibabacloud.com/help/en/model-studio/token-plan-team-faq), capture `cloud-en-token-plan-team-faq.txt`: dynamic concurrency and no downgrade.
- [EN Team management](https://www.alibabacloud.com/help/en/model-studio/token-plan-team-management), capture `cloud-en-token-plan-team-management.txt`: member removal and shared-pack cap.
- [CN Personal overview](https://platform.qianwenai.com/docs/token-plan/personal/overview) and [EN Personal overview](https://docs.qwencloud.com/token-plan/personal/overview): separately captured supported-tool lists.

These are vendor policy claims, not newly measured credit coefficients or account health. No paid inference was used for this update.
