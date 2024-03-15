from abc import ABC, abstractmethod

from dataclasses import dataclass

@dataclass
class A:
    a: int

a = A(1)
b = A(2)

d = {"a": a}
d1 = {"a": a}

a.a = b.a

print(d, d1)
