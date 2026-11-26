import { initializeTestEnvironment, assertSucceeds, assertFails } from "@firebase/rules-unit-testing";
import { readFileSync } from "fs";
import { doc, getDoc, setDoc, getDocs, collection, query, where, addDoc, serverTimestamp, updateDoc, deleteDoc } from "firebase/firestore";

const env = await initializeTestEnvironment({ projectId: "demo-wb", firestore: { rules: readFileSync(process.argv[2], "utf8"), host: "127.0.0.1", port: 8080 } });
const as = (email) => env.authenticatedContext(email, { email, email_verified: true }).firestore();
const anon = env.unauthenticatedContext().firestore();
const owner = as("M.Jaberi1212@gmail.com"), psy = as("psy@x.nl"), hr = as("hr@acme.nl"), hr2 = as("hr@other.nl"), mgr = as("mgr@acme.nl"), mgr2 = as("mgr2@acme.nl"), stranger = as("who@x.nl");
const unverified = env.authenticatedContext("u", { email: "hr@acme.nl", email_verified: false }).firestore();
let pass = 0, fail = 0;
const t = async (name, p) => { try { await p; pass++; } catch (e) { fail++; console.log("FAIL:", name, e.message.split("\n")[0]); } };

await env.withSecurityRulesDisabled(async c => {
  const d = c.firestore();
  await setDoc(doc(d, "members/psy@x.nl"), { role: "psy", active: true });
  await setDoc(doc(d, "members/hr@acme.nl"), { role: "hr", orgs: ["acme"], active: true });
  await setDoc(doc(d, "members/hr@other.nl"), { role: "hr", orgs: ["other"], active: true });
  await setDoc(doc(d, "members/mgr@acme.nl"), { role: "mgr", orgs: ["acme"], units: ["uops", "uwh"], active: true });
  await setDoc(doc(d, "members/mgr2@acme.nl"), { role: "mgr", orgs: ["acme"], units: ["usal"], active: false });
  await setDoc(doc(d, "rounds/ABCD-EFGH-JKLM"), { orgId: "acme", org: "Acme", status: "open", unitIds: ["uops", "uwh", "usal"] });
  await setDoc(doc(d, "unitreports/ABCD-EFGH-JKLM__uops"), { orgId: "acme", unitId: "uops", agg: {} });
  await setDoc(doc(d, "unitreports/ABCD-EFGH-JKLM__uwh"), { orgId: "acme", unitId: "uwh", agg: {} });
  await setDoc(doc(d, "unitreports/ABCD-EFGH-JKLM__usal"), { orgId: "acme", unitId: "usal", agg: {} });
  await setDoc(doc(d, "unitreports/OTHERRND__uops"), { orgId: "other", unitId: "uops", agg: {} });
  await setDoc(doc(d, "rounds/CLOS-EDXX-XXXX"), { orgId: "acme", status: "closed" });
  await setDoc(doc(d, "rounds/OLDR"), { org: "Old" });
  await setDoc(doc(d, "responses/r1"), { r: "ABCD-EFGH-JKLM", lv: "staff", a: {} });
  await setDoc(doc(d, "reports/ABCD-EFGH-JKLM"), { orgId: "acme", agg: {} });
  await setDoc(doc(d, "reports/OTHERRND"), { orgId: "other", agg: {} });
  await setDoc(doc(d, "orgs/acme"), { name: "Acme" });
  await setDoc(doc(d, "partners/p1"), { name: "A", published: true });
  await setDoc(doc(d, "partners/p2"), { name: "B", published: false });
  await setDoc(doc(d, "applications/a1"), { name: "x" });
  await setDoc(doc(d, "leads/l1"), { org: "x" });
});

const resp = { v: 1, r: "ABCD-EFGH-JKLM", lv: "staff", p: "standard", m: "2026-11", a: { scs: [1, 2, 3] } };
// participants
await t("anon can answer open round", assertSucceeds(setDoc(doc(anon, "responses/n1"), resp)));
await t("anon cannot answer closed round", assertFails(setDoc(doc(anon, "responses/n2"), { ...resp, r: "CLOS-EDXX-XXXX" })));
await t("old round without status counts as open", assertSucceeds(setDoc(doc(anon, "responses/n3"), { ...resp, r: "OLDR" })));
await t("anon cannot answer unknown round", assertFails(setDoc(doc(anon, "responses/n4"), { ...resp, r: "NOPE" })));
await t("extra field rejected", assertFails(setDoc(doc(anon, "responses/n5"), { ...resp, email: "a@b.c" })));
await t("anon cannot read answers", assertFails(getDoc(doc(anon, "responses/r1"))));
await t("hr cannot read answers", assertFails(getDoc(doc(hr, "responses/r1"))));
await t("hr cannot list answers", assertFails(getDocs(query(collection(hr, "responses"), where("r", "==", "ABCD-EFGH-JKLM")))));
await t("psy can list answers", assertSucceeds(getDocs(query(collection(psy, "responses"), where("r", "==", "ABCD-EFGH-JKLM")))));
await t("owner (any case) can read answers", assertSucceeds(getDoc(doc(owner, "responses/r1"))));
await t("nobody edits answers", assertFails(updateDoc(doc(owner, "responses/r1"), { lv: "x" })));
await t("psy cannot delete answers", assertFails(deleteDoc(doc(psy, "responses/r1"))));
// departments
await t("anon answers with a known department", assertSucceeds(setDoc(doc(anon, "responses/u1"), { ...resp, u: "uwh" })));
await t("unknown department rejected", assertFails(setDoc(doc(anon, "responses/u2"), { ...resp, u: "uxx" })));
await t("department on a round without departments rejected", assertFails(setDoc(doc(anon, "responses/u3"), { ...resp, r: "OLDR", u: "uwh" })));
await t("department must be a short string", assertFails(setDoc(doc(anon, "responses/u4"), { ...resp, u: ["uwh"] })));
await t("mgr reads own department report", assertSucceeds(getDoc(doc(mgr, "unitreports/ABCD-EFGH-JKLM__uwh"))));
await t("mgr cannot read other department", assertFails(getDoc(doc(mgr, "unitreports/ABCD-EFGH-JKLM__usal"))));
await t("mgr cannot read same unit id in other org", assertFails(getDoc(doc(mgr, "unitreports/OTHERRND__uops"))));
await t("mgr lists own departments", assertSucceeds(getDocs(query(collection(mgr, "unitreports"), where("orgId", "==", "acme"), where("unitId", "in", ["uops", "uwh"])))));
await t("mgr cannot list whole org", assertFails(getDocs(query(collection(mgr, "unitreports"), where("orgId", "==", "acme")))));
await t("inactive mgr gets nothing", assertFails(getDoc(doc(mgr2, "unitreports/ABCD-EFGH-JKLM__usal"))));
await t("mgr cannot read org report", assertFails(getDoc(doc(mgr, "reports/ABCD-EFGH-JKLM"))));
await t("mgr cannot read answers", assertFails(getDoc(doc(mgr, "responses/r1"))));
await t("mgr cannot read org doc", assertFails(getDoc(doc(mgr, "orgs/acme"))));
await t("mgr cannot list rounds", assertFails(getDocs(query(collection(mgr, "rounds"), where("orgId", "==", "acme")))));
await t("mgr cannot write department report", assertFails(setDoc(doc(mgr, "unitreports/ABCD-EFGH-JKLM__uwh"), { orgId: "acme", unitId: "uwh", agg: { x: 1 } })));
await t("hr reads any own-org department report", assertSucceeds(getDocs(query(collection(hr, "unitreports"), where("orgId", "==", "acme")))));
await t("hr2 cannot read acme department report", assertFails(getDoc(doc(hr2, "unitreports/ABCD-EFGH-JKLM__uwh"))));
await t("psy writes department report", assertSucceeds(setDoc(doc(psy, "unitreports/X__u"), { orgId: "acme", unitId: "u" })));
await t("mgr writes own audit row", assertSucceeds(addDoc(collection(mgr, "audit"), { by: "mgr@acme.nl", at: serverTimestamp(), act: "view" })));
// action plans
const plan = { orgId: "acme", roundId: "ABCD-EFGH-JKLM", items: [{ id: "a1", unit: "uwh", action: "x", status: "planned" }], share: false, updatedAt: serverTimestamp(), by: "hr@acme.nl" };
await t("hr creates own-org plan", assertSucceeds(setDoc(doc(hr, "plans/ABCD-EFGH-JKLM"), plan)));
await t("hr2 cannot write acme plan", assertFails(setDoc(doc(hr2, "plans/ABCD-EFGH-JKLM"), { ...plan, by: "hr@other.nl" })));
await t("plan orgId must match round", assertFails(setDoc(doc(hr2, "plans/ABCD-EFGH-JKLM"), { ...plan, orgId: "other" })));
await t("plan with extra key rejected", assertFails(setDoc(doc(psy, "plans/ABCD-EFGH-JKLM"), { ...plan, secret: 1 })));
await t("plan for unknown round rejected", assertFails(setDoc(doc(psy, "plans/NOPE"), { ...plan, roundId: "NOPE" })));
await t("anon cannot read unshared plan", assertFails(getDoc(doc(anon, "plans/ABCD-EFGH-JKLM"))));
await t("mgr reads own-org plan", assertSucceeds(getDoc(doc(mgr, "plans/ABCD-EFGH-JKLM"))));
await t("mgr cannot write plan", assertFails(setDoc(doc(mgr, "plans/ABCD-EFGH-JKLM"), { ...plan, by: "mgr@acme.nl" })));
await t("psy shares plan", assertSucceeds(setDoc(doc(psy, "plans/ABCD-EFGH-JKLM"), { ...plan, share: true })));
await t("anon reads shared plan", assertSucceeds(getDoc(doc(anon, "plans/ABCD-EFGH-JKLM"))));
await t("anon cannot list plans", assertFails(getDocs(query(collection(anon, "plans"), where("orgId", "==", "acme")))));
await t("hr lists own-org plans", assertSucceeds(getDocs(query(collection(hr, "plans"), where("orgId", "==", "acme")))));
await t("hr cannot delete plan", assertFails(deleteDoc(doc(hr, "plans/ABCD-EFGH-JKLM"))));
await t("anon cannot write plan", assertFails(setDoc(doc(anon, "plans/ABCD-EFGH-JKLM"), plan)));
// rounds
await t("anon can get a round", assertSucceeds(getDoc(doc(anon, "rounds/ABCD-EFGH-JKLM"))));
await t("anon cannot list rounds", assertFails(getDocs(collection(anon, "rounds"))));
await t("hr lists own org rounds", assertSucceeds(getDocs(query(collection(hr, "rounds"), where("orgId", "==", "acme")))));
await t("hr cannot list other org rounds", assertFails(getDocs(query(collection(hr, "rounds"), where("orgId", "==", "other")))));
await t("psy cannot create round", assertFails(setDoc(doc(psy, "rounds/NEW"), { orgId: "acme" })));
await t("owner creates round", assertSucceeds(setDoc(doc(owner, "rounds/NEW"), { orgId: "acme", status: "open" })));
// reports
await t("hr reads own report", assertSucceeds(getDoc(doc(hr, "reports/ABCD-EFGH-JKLM"))));
await t("hr cannot read other report", assertFails(getDoc(doc(hr, "reports/OTHERRND"))));
await t("hr lists own reports", assertSucceeds(getDocs(query(collection(hr, "reports"), where("orgId", "==", "acme")))));
await t("hr cannot list all reports", assertFails(getDocs(collection(hr, "reports"))));
await t("hr cannot write report", assertFails(setDoc(doc(hr, "reports/ABCD-EFGH-JKLM"), { orgId: "acme", agg: { fake: 1 } })));
await t("psy writes report notes", assertSucceeds(updateDoc(doc(psy, "reports/ABCD-EFGH-JKLM"), { notes: "ok" })));
await t("unverified e-mail gets nothing", assertFails(getDoc(doc(unverified, "reports/ABCD-EFGH-JKLM"))));
await t("stranger signed in gets nothing", assertFails(getDoc(doc(stranger, "reports/ABCD-EFGH-JKLM"))));
// orgs & members
await t("hr reads own org", assertSucceeds(getDoc(doc(hr, "orgs/acme"))));
await t("hr2 cannot read acme", assertFails(getDoc(doc(hr2, "orgs/acme"))));
await t("hr cannot make self admin", assertFails(setDoc(doc(hr, "members/hr@acme.nl"), { role: "admin" })));
await t("hr reads own member doc", assertSucceeds(getDoc(doc(hr, "members/hr@acme.nl"))));
await t("owner adds member", assertSucceeds(setDoc(doc(owner, "members/new@x.nl"), { role: "hr", orgs: ["acme"], active: true })));
// leads / applications
const lead = { org: "Beta BV", email: "hr@beta.nl", name: "Sam", profile: { size: ["s3"] }, pkg: "complete", items: ["copsoq"], lang: "nl", status: "new", createdAt: serverTimestamp() };
await t("anon sends lead", assertSucceeds(addDoc(collection(anon, "leads"), lead)));
await t("lead bad email", assertFails(addDoc(collection(anon, "leads"), { ...lead, email: "nope" })));
await t("lead must be new", assertFails(addDoc(collection(anon, "leads"), { ...lead, status: "won" })));
await t("anon cannot read leads", assertFails(getDoc(doc(anon, "leads/l1"))));
await t("psy cannot read leads", assertFails(getDoc(doc(psy, "leads/l1"))));
const app = { name: "Dr. A", email: "a@b.nl", bio: "Hello", c1: true, c2: false, c3: true, role: ["psy"], lang: ["fa", "nl"], reg: "nip", uiLang: "fa", status: "new", createdAt: serverTimestamp() };
await t("anon sends application", assertSucceeds(addDoc(collection(anon, "applications"), app)));
await t("application needs consent", assertFails(addDoc(collection(anon, "applications"), { ...app, c1: false })));
await t("application bio limit", assertFails(addDoc(collection(anon, "applications"), { ...app, bio: "x".repeat(601) })));
await t("anon cannot read applications", assertFails(getDoc(doc(anon, "applications/a1"))));
await t("owner reads applications", assertSucceeds(getDoc(doc(owner, "applications/a1"))));
// partners
await t("anon lists published partners", assertSucceeds(getDocs(query(collection(anon, "partners"), where("published", "==", true)))));
await t("anon cannot list all partners", assertFails(getDocs(collection(anon, "partners"))));
await t("anon cannot read draft partner", assertFails(getDoc(doc(anon, "partners/p2"))));
// group files & audit
await t("anon gets group file", assertSucceeds(getDoc(doc(anon, "groupfiles/abc"))));
await t("anon cannot write group file", assertFails(setDoc(doc(anon, "groupfiles/abc"), { ct: "x" })));
await t("psy writes group file", assertSucceeds(setDoc(doc(psy, "groupfiles/abc"), { ct: "x" })));
await t("hr writes own audit row", assertSucceeds(addDoc(collection(hr, "audit"), { by: "hr@acme.nl", at: serverTimestamp(), act: "view" })));
await t("hr cannot forge audit", assertFails(addDoc(collection(hr, "audit"), { by: "m.jaberi1212@gmail.com", at: serverTimestamp(), act: "x" })));
await t("hr cannot read audit", assertFails(getDocs(collection(hr, "audit"))));
console.log(`passed ${pass}, failed ${fail}`);
await env.cleanup();
process.exit(fail ? 1 : 0);
