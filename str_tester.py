strf = "FFF.png"
strf = strf.split('.')
strf[0] = strf[0] + "_{}"
print(".".join(strf).format("323"))