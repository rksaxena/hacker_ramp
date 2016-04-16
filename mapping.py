import json
import pprint, operator

ref_list = {}
with open("Article_type.txt","r") as f:
    c = f.readlines()

for k in c:
    ref_list[(k.rstrip()).lower()] = True

#print len(ref_list)
#with open("amazon_color_list.json") as af:
#    acl = json.load(af)

#print len(acl["colour"])

count = 0
import re
import HTMLParser
h = HTMLParser.HTMLParser()
not_found = {}
found_in_color_list = {}
#1. Check if the key name already exists
for k in acl["colour"]:
    k = h.unescape(k)
    kl = re.split(",|/|and|&|;|:", k)
    for kvl in kl:
        kvl = kvl.encode("ascii", "ignore")
        kv = re.sub('[^A-Za-z]+', '', kvl)
        if kv.strip() in ref_list:
            count +=1
            found_in_color_list[kv.strip()] = kv.strip()
        else:
            kv = kv.replace(" ","")
            if kv.strip() in ref_list:
                count +=1
            else:
                if kvl.strip() not in not_found:
                    not_found[kvl.strip()] = 0
                not_found[kvl.strip()] +=1

#print "Number of keys not found %s" %(len(not_found.keys()))
#print "Number of keys found %s" %count
#print json.dumps(found_in_color_list)
#2. After inital mapping try the remaining keys with CMS mapping
#print "Starting second step..."
with open("cms_color_map") as f:
    cms_color_map = json.load(f)

not_found_cms= {}
found_in_cms_map = {}
for kvl in not_found:
    kv = re.sub('[^A-Za-z]+', '', kvl)
    kv = kv.replace(" ","") 
    if kv.strip() in cms_color_map:
        found_in_cms_map[kv.strip()] = cms_color_map[kv.strip()]
    else:
        if kvl.strip() not in not_found_cms:
            not_found_cms[kvl.strip()] = 0
        not_found_cms[kvl.strip()] +=1

#print "Number of keys not found in CMS map %s" %(len(not_found_cms.keys()))
#print "Number of keys found in CMS map %s" %found_in_cms_map
#print json.dumps(found_in_cms_map)

#3. Try partial mapping
#print "Starting step 3..."
partial_map_ct = 0
no_partial_map = {}
partial_map = {}
for key in not_found_cms:
    ks = key.split(" ")
    f = False
    for k in ks:
        for r in ref_list:
            if r in k:
                partial_map_ct += 1
                ks =  " ".join(ks)
                partial_map[ks] = r 
                f = True
                break
        if f:
            break
        
        # Check in CMS Mapping
        if not f:
            if k in cms_color_map:
                partial_map_ct +=1
                ks = " ".join(ks)
                partial_map[ks] = cms_color_map[k]
                f = True
                break
    if not f:
        ks = " ".join(ks)
        if ks not in no_partial_map:
            no_partial_map[ks] = 0
        no_partial_map[ks] +=1

#print json.dumps(no_partial_map)
#print json.dumps(partial_map)
#print "Number of keys not found in partial_map %s" %(len(no_partial_map.keys()))
#print "Number of keys found in partial_map %s" %partial_map_ct

#4. Try distance based similarity with the known keys

known_keys = ref_list.keys() + cms_color_map.keys()
#print "Starting step 4..."
ct_dist = 0
no_dist_map = {}
dist_map = {}
for key in no_partial_map:
    found = False
    for kk in known_keys:
        ed = editdistance.eval(key,kk)
        if ed <=1 or (ed<=3 and sorted(kk) == sorted(key)):
            dist_map[key] = kk
            ct_dist +=1
            found = True
            break
    if not found:
        no_dist_map[key] = True

#print json.dumps(dist_map)
#print "Number of keys found similar %s" %ct_dist
#print "Number of keys not found similar %s" %(len(no_dist_map.keys()))

full_color_map = {}
full_color_map["direct_map"] = found_in_color_list 
full_color_map["cms_map"] = found_in_cms_map
full_color_map["partial_map"] = partial_map
full_color_map["dist_map"] = dist_map

print json.dumps(full_color_map)
