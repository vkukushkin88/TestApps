
from multiprocessing.pool import ThreadPool


def get_pool(threads_number):
    return ThreadPool(threads_number)


    # thread_pool = get_pool(2)
    # thread_results = []

    #     thread_results.append(thread_pool.apply_async(xml_generator.generate_xml_file))

    # for thread_result in thread_results:
        # zipf.write(thread_result.get())
        # zipf.writestr(*thread_result.get())
