from cache import lru_cache
import time
import datetime

if __name__ == '__main__':
    try:
        o = lru_cache()

        # Test 1
        print("\nTest 1, add 6 entires to the cache")

        o.put("a", "aa")
        o.put("b", "bb")
        o.put("c", "cc")
        time.sleep(0.5)
        o.put("d", "dd")
        o.put("e", "ee")
        o.put("f", "ff")
        
        for e in o.view():
            print(e)

        # Test 2
        print("\nTest 2, get key 'c' once")
        print(o.get('c'))

        # Test 3
        print("\nTest 3, check the new cache order")
        for e in o.view():
            print(e)
        
        # Test 4
        print("\nTest 4, delete expired entries (0.5 seconds)")
        o.removeExpired(0.5)
        for e in o.view():
            print(e)

    except Exception as e: 
        print(e)