/**
 * @name Possible mocked hardcoded data
 * @id python/mocked-hardcoded-data
 * @kind problem
 * @problem.severity warning
 */

import python

from StringLiteral s
where
  s.getValue().matches("%test@%") or
  s.getValue().matches("%example.com%") or
  s.getValue().matches("%mock%") or
  s.getValue().matches("%fake%") or
  s.getValue().matches("%dummy%") or
  s.getValue().matches("%123.456.789-00%")
select s, "Possível dado mockado hardcoded"
