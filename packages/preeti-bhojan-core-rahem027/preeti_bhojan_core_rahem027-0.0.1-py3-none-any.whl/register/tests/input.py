"""
Sample inputs for different types of input like alphabetic, alphanumeric, etc.
"""
alphabetic = {
  'abc': True,
  'abc ': False,
  'abc \t\r\n': False,
  'a bc': False,
  '123': False,
  'abc123': False,
  'abc 123': False,
  '': False,
  ' ': False,
  '\t': False,
  '\t\r': False
}

alphaNumeric = {
  'abc': True,
  '123': True,
  'abc123 ': True,
  'abc \t\r\n': False,
  'abc132\t\r\n': False,
  'a bc': False,
  'abc 123': False,
  'abc 12344 ': False,
  '': False,
  ' ': False,
  '\t': False,
  '\t\r': False
}

numeric = {
  '123': True,
  ' 123': False,
  '1233 ': False,
  '123 \t\r\n': False,
  'a': False,
  ' a': False,
  ')(*&^': False,
  '\t': False,
  '\t\r': False
}

alphaNumericWithSpacesAndUnderscore = {
  'abc': True,
  'a bc': True,
  '123': True,
  'abc123': True,
  'abc 123': True,
  'abc_123 def': True,
  'abc 12334_': True,
  'abc 12334_ \t\r\n': True,
  '': False,
  ' ': False,
  '\t': False,
  '\t\r': False
}

phoneNumbers = {
  '1234567890': True,
  '1234567890\t\r\n': False,
  '-1234567890': False,
  'a': False,
  '': False,
  '1': False,
  '+911234567890': False,
  '+1234567890': False,
  '-%18963691': False,
}
