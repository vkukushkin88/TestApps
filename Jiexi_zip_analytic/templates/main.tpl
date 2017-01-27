@require(uniq_string_value, rand_number, random_strings)
<root>
    <var name='id' value='@uniq_string_value'/>
    <var name='level' value='@rand_number'/>
    <objects>
        @for random_string in random_strings:
        <object name='@random_string'/>
        @end
    </objects>
</root>
