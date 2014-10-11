---
title: Address forms suck
created_at: 2014-04-26
kind: article
tags: [ 'UX', 'rant' ]
---

<div class="wide"><img alt="It is an address form for illustration" src="http://f.codl.fr/1404/0BKNBl.png" /></div>

I was looking at a package I got the other day and noticed the order of the address was wrong.

Addresses have very different formats in each country, yet every single website still asks me for my “State/Region”.
This field is completely useless here in France, and many other countries.
Sometimes it's a text box, and I don't know if I can leave it empty or if I have to input “N/A” or something else that will look stupid once printed on the package.
Sometimes it's a drop-down list and I have to hunt down either the “Non-US” option, or maybe it was filled with French regions or French departments once I picked my country.
I then have to guess which of the two it loaded and find my region or department accordingly, even though it will never be used by *La Poste*.
In some extreme cases, there is no “Non-US” option and I have to pick a random US state just to continue.

And that's just one field! Let me make a quick list of other gripes I have with usual address input forms:

* Postal codes don't even exist in some countries.
* Many people here live in *lieux-dits* and don't have a street name.
* Let's not even mention separating first and last names, [the issue has been explored to hell and back already](http://www.w3.org/International/questions/qa-personal-names).

### A proposal

So here's my idea for a next-generation address form:

    <textarea name='address'></textarea>

And here it is in action:

<div><textarea cols='30' rows='4' name='address'></textarea></div>

I know how to type my full address. I know the syntax of French addresses. You probably do not. You certainly do not know every single country's address format.
So why do you insist on taking my address in parts and then cobbling it back together?

There are no meaningful operations you can do on my broken down address bits that you can't do on my full formatted address. The only thing I can think of is choosing a different shipping company based on my country, or maybe deciding that you don't ship to my country, so I'll accept a country dropdown separate to the address.
But, honestly, do you really need my “Address line 2” to be separate from my “Address line 1?”

Just let me handle my address, I know it better than you do.

---

PS: You should also get your encoding and escaping right. I don't live in *rue CuirassÃ© Bretagne*, nor *rue Cuirass&amp;eacute; Bretagne*.
